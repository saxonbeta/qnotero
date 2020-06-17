Qnotero v2.2.0


&copy; 2020 E. Albiter

## Overview


- [What is Qnotero?](#what-is-qnotero)
- [Download and installation](#download-and-installation)
- [Dependencies](#dependencies)
- [Gnote integration (Linux only)](#gnote-integration-linux-only)


## What is Qnotero?

Qnotero provides lightning quick access to your Zotero references. Zotero is an excellent open source reference manager, but it lacks a simple and direct way to access your references at the click of a button. Qnotero lives in the system tray and allows you to search through your references by Author, Year of Publication, and/or DOI. If a PDF file is attached to a reference you can open it directly from within Qnotero, if not the URL of the reference is opened instead.

Freely available under the [GNU GPL 3](http://www.gnu.org/copyleft/gpl.html).

## Download and installation

Visit the [installation page](https://github.com/ealbiter/qnotero/wiki/Installation)

## Dependencies

Qnotero has the following dependencies.

- [Python] -- As of Qnotero 1.0.0, Python >= 3.3 is required.
- [PyQt5] -- Pass `--qt4` as command-line argument for PyQt4 legacy support.

## Gnote integration (Linux only)

If you have Gnote installed (a note-taking program for Linux), Qnotero automatically searches Gnote for a (section in a) note belonging to a specific article. Qnotero expects each note to be preceded by a bold line containing at least the name of the first author and the year of publication within parentheses, like so:

    Duhamel et al. (1992) Science 255

[python]: https://www.python.org/
[PyQt5]: http://www.riverbankcomputing.co.uk/software/pyqt/download

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/qnotero)

[Overview]: #overview
[What is Qnotero?]: #what-is-qnotero
[Download and installation]: #download-and-installation
[Dependencies]: #dependencies
[Gnote integration (Linux only)]: #gnote-integration-linux-only