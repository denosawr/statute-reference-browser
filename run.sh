pandoc "$1" -f docx -t html -o index.html -s --metadata title="ACL" --css=style.css --filter ./filter.py --template template.html

zip dist.zip template.html style.css script.js