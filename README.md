# data-labelling-webapp

This is a data labelling inferface built in Flask, JS, HTML, CSS, Bootstrap.

The UI is integrated with a Machine Learning Model on the back-end, which classifies scene images using snorkel framework and weak supervision approaches.

The model is trained on a very minimal data and achieves an accuracy of 92%.
***

Input
---
1. Unlabelled scene image/(s)

Output
---
1. Labelled image 
2. Zip file of labelled dataset that can be downloaded
***

Run
---
```Javascript
python main.py
```
***

Served on
---

```Javascript
http://127.0.0.1:5000/
```

---

