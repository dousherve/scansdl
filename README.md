# scans_dl
A (very basic) tool to download all the manga scans in a webpage.

For now, the code is pretty stupid and just looks for every HTML `<img>` tag in the webpage at the given URL, and then downloads all those images.

First, install the dependencies (make sure to create and activate a virtual environment beforehand if you don't want to clutter your main Python install) :

```console
python3 -m pip install -r requirements.txt
```

To use the "library", one can write something like that :

```python3
import scans_dl

scans_dl.download("https://site.com/url/of/the/manga")
```

By default, it will download the scans in a new directory named `scans`.  

You can override that behavior by passing an additional argument to the `download` function :
```python3
scans_dl.download("https://site.com/url/of/the/manga", "my-scans-folder")
```

Of course, use this tool only if you already own a physical copy of the manga! 🤓
