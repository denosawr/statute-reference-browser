#!/usr/bin/env python

from panflute import run_filters, TableRow, stringify, Para, Str, Space, Link
import re
import sys


def printf(*values):
    for v in values:
        sys.stderr.write(f"{v} ")
    sys.stderr.write("\n")


sectionIdLookup = {}


def processSectionIds(id_strings):
    bulk_pattern = r"(.+?)\s*(?:,|$)"
    section_pattern = r"(\w+)"
    numerical_pattern = r"(\d+)"

    section_groups = re.findall(bulk_pattern, id_strings)

    all_sections = set()
    id = None
    for section_group in section_groups:
        sections = re.findall(section_pattern, section_group)
        if not id:
            id = sections[0]

        all_sections = all_sections.union(sections)

        numerical_sections = [
            int(x) for x in re.findall(numerical_pattern, section_group)
        ]
        if len(numerical_sections) > 1:
            min_number = min(numerical_sections)
            max_number = max(numerical_sections)

            all_sections = all_sections.union(
                str(x) for x in range(min_number, max_number + 1)
            )

    return (id, tuple(all_sections))


def processSectionRefs(elem):
    # printf("==========")
    last_item = None

    s_regex = r"\W*[sS]{1,2}\s*$"
    d_regex = r"(\d+)"

    if not hasattr(elem, "content"):
        return elem

    oldContent = elem.content
    elem.content = []

    for item in oldContent:
        is_str = isinstance(item, Str)
        is_space = isinstance(item, Space)

        # printf(item)
        if not (is_str or is_space):
            # printf("OH NO", item)
            elem.content.append(processSectionRefs(item))
            continue

        contents = stringify(item)
        if is_str:
            matches = re.findall(d_regex, contents)

            if last_item:
                pairing = (last_item, Space(), item)
                if matches:
                    # find valid id element
                    found_match = False
                    for id, sections in sectionIdLookup.items():
                        if matches[0] in sections:
                            link_elem = Link(
                                *pairing,
                                url=f"#{id}",
                                classes=["section-link"],
                            )

                            elem.content.append(link_elem)
                            found_match = True
                            break

                    if not found_match:
                        printf("NOT FOUND", matches, pairing)
                        elem.content.extend(pairing)

                else:
                    elem.content.extend(pairing)
                last_item = None

            elif re.match(s_regex, contents):
                # case 1: "s131", contains both matches
                if matches:
                    found_match = False
                    for id, sections in sectionIdLookup.items():
                        if matches[0] in sections:
                            link_elem = Link(
                                item, url=f"#{id}", classes=["section-link"]
                            )

                            elem.content.append(link_elem)
                            found_match = True
                            break

                    if not found_match:
                        printf("NOT FOUND", matches, item)
                        elem.content.append(item)
                    last_item = None

                # case 2: "s 131" i.e. wait until next match
                last_item = item

            else:
                elem.content.append(item)

        elif is_space and last_item:
            continue
        else:
            elem.content.append(item)

    return elem


def tableIds(elem, doc):
    if isinstance(elem, TableRow):
        # get contents of first column
        section_labels = stringify(elem.content[0])
        if not section_labels:
            elem.classes.append("notes-row")
            return None

        id, sections = processSectionIds(section_labels)
        sectionIdLookup[id] = sections

        elem.attributes["id"] = id
    return None


def makeSectionLinks(elem, doc):
    if isinstance(elem, Para):
        return processSectionRefs(elem)
    return None


def main(doc=None):
    return run_filters((tableIds, makeSectionLinks), doc=doc)


if __name__ == "__main__":
    main()
