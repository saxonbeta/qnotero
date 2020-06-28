Qnotero v2.3.0


&copy; 2020 E. Albiter

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/qnotero)


## What is Qnotero?

Qnotero provides lightning-quick access to your Zotero references. Zotero is an excellent open-source reference 
manager, but it lacks a direct and straightforward way to access your references at the click of a button. 
Qnotero lives in the system tray and allows you to search through your references by author, 
year of Publication, and DOI. If a PDF file is attached to a reference, you can open it directly from within Qnotero; 
if not, the URL of the reference is opened instead. You can also copy some basic information
of the reference, such as DOI, title, authors, and abstract.

Freely available under the [GNU GPL 3].

## Download and installation

Visit the [installation page]

## Dependencies

Qnotero has the following dependencies.

- [Python] -- As of Qnotero 1.0.0, Python >= 3.3 is required.
- [PyQt5] -- Pass `--qt4` as command-line argument for PyQt4 legacy support.

## Gnote integration (Linux only)

If you have Gnote installed (a note-taking program for Linux), Qnotero automatically searches Gnote 
for a (section in a) note belonging to a specific article. Qnotero expects each note to be preceded 
by a bold line containing at least the name of the first author and the year of publication within 
parentheses, like so:

    Duhamel et al. (1992) Science 255


[Python]: https://www.python.org/
[PyQt5]: https://riverbankcomputing.com/software/pyqt/
[installation page]: https://github.com/ealbiter/qnotero/wiki/Installation
[GNU GPL 3]: http://www.gnu.org/copyleft/gpl.html

