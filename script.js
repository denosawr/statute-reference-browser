let hist;

let updateAnchor = (anchor) => {
  history.pushState(
    '',
    document.title,
    window.location.pathname + anchor + window.location.search
  );

  
};

let scrollToElem = (elem, updateHref, updateHistory) => {
  document.getElementById(elem).scrollIntoView({ block: 'center' });
  if (updateHref) {
    updateAnchor('#' + elem);
  }

  if (updateHistory) {
    // check if this element already exists in the list
    for (let item of [...hist.children]) {
      item.classList.remove("selected");
      if (item.children[0].href.endsWith(`${elem}`)) {
        item.remove();
      }
    }

    let elemObj = document.getElementById(elem);
    let sectionLabel = elemObj.children[0].textContent;
    let contents = elemObj.children[1].textContent.split('\n')[0];
  

    // needs two new elements
    let li = document.createElement("li");
    li.classList.add("selected");
    let cur = document.createElement("a");
    cur.href = `#${elem}`
    cur.classList.add("history-link")
    cur.innerHTML = `s ${sectionLabel}: ${contents}`

    cur.onclick = (e) => {
      e.preventDefault();

      for (let item of [...hist.children]) {
        if (item.children[0].href.endsWith(`${elem}`)) {
          item.classList.add("selected");
        } else {
          item.classList.remove("selected");
        }
      }

      scrollToElem(elem, false, false);
    }

    li.append(cur);
    hist.append(li);
  }
};

window.onload = () => {
  hist = document.querySelector("#history-list");
  console.log(hist)

  let links = document.querySelectorAll("a.section-link");
  for (let link of links) {
    let anchor = link.getAttribute("href").slice(1);
    
    link.onclick = (e) => {
      e.preventDefault();
      console.log("CLICK!", anchor);

      scrollToElem(anchor, false, true);
    }
  }
}
