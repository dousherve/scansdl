# scansdl
A basic tool written in Python to download all the manga scans in a webpage. The tool does *not* run on Windows yet!

For now, the code is pretty stupid and just looks for every HTML `<img>` tag in the webpage at the given URL, and then downloads all those images.

Use this to install the program (make sure to create and activate a virtual environment beforehand if you don't want to clutter your main Python install) :

```console
python3 -m pip install "git+https://github.com/dousherve/scansdl#egg=scansdl"
```

To use the program, one can write something like that :

```console
scansdl download https://site.com/chapter-1
```

This command downloads all the scans of the chapter found in the webpage. It doesn't work if the website you provide has a reader where you have to turn the pages yourself.

You can also download multiple chapters at a time, by replacing the number of the chapter that changes in the address with '{}' and by specifying a range. For instance:

```console
scansdl download https://site.com/chapter-{} --range 1-40
```
or, in short:
```console
scansdl dl https://site.com/chapter-{} -r 40
```

downloads the chapters 1 to 40, where the chapter number is replacing the `{}` in the URL.

By default, it will download the scans in new directories: `scans/raw`.  

You can override that behavior by passing an additional argument:

```console
scansdl download https://site.com/chapter-1 --output [folder]
```
or, in short:
```console
scansdl dl https://site.com/chapter-1 -o [folder]
```

To archive a chapter in the CBR format, you can use that command:

```console
scansdl cbr path/to/folder/containing/scans
```

To archive all chapters contained in a folder, you can use that command:

```console
scansdl cbr --all path/to/folder/containing/all/chapters
```

By default, it will save the archive(s) in new directories: `scans/cbr`.  

For the complete documentation, use:

```console
scansdl --help
```
along with the command which you are interested in, for instance `download` or `cbr`.

Of course, use this tool only if you already own a physical copy of the chapter you're downloading! 🤓
