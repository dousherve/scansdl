# scans_dl
A basic tool written in Python to download all the manga scans in a webpage.

For now, the code is pretty stupid and just looks for every HTML `<img>` tag in the webpage at the given URL, and then downloads all those images.

First, install the dependencies (make sure to create and activate a virtual environment beforehand if you don't want to clutter your main Python install) :

```shell
python3 -m pip install -r requirements.txt
```

To use the program, one can write something like that :

```shell
python3 scans_dl.py download https://site.com/chapter-1
```

This command downloads all the scans of the chapter found in the webpage. It doesn't work if the website you provide has a reader where you have to turn the pages yourself.

You can also download multiple chapters at a time, by replacing the number of the chapter that changes in the address with '{}' and by specifying a range. For instance:

```shell
python3 scans_dl.py download https://site.com/chapter-{} --range 1-40
```

downloads the chapters 1 to 40.

By default, it will download the scans in a new directory named `scans/raw`.  

You can override that behavior by passing an additional argument:

```console
python3 scans_dl.py download https://site.com/chapter-1 --output [folder]
```


To archive a chapter in the CBR format, you can use that command:

```console
python3 scans_dl.py cbr path/to/folder/containing/scans
```

By default, it will save the archive in a new directory named `scans/cbr`.  

For the complete documentation, use:

```console
python3 scans_dl.py --help
```
along with the command which you are interested in, for instance `download` or `cbr`.

Of course, use this tool only if you already own a physical copy of the chapter you're downloading! 🤓
