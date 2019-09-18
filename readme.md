Qnotero v2.1.0


## Overview


- [What is Qnotero?](#what-is-qnotero)
- [Download and installation](#download-and-installation)
	- [Windows](#windows)
	- [Linux](#linux)
	- [mac OS](#mac-os)
	- [Other operating systems](#other-operating-systems)
- [Dependencies](#dependencies)
- [Gnote integration (Linux only)](#gnote-integration-linux-only)


## What is Qnotero?

Qnotero provides lightning quick access to your Zotero references. Zotero is an excellent open source reference manager, but it lacks a simple and direct way to access your references at the click of a button. Qnotero lives in the system tray and allows you to search through your references by Author, Year of Publication, and/or DOI. If a PDF file is attached to a reference you can open it directly from within Qnotero, if not the URL of the reference is opened instead.

Freely available under the [GNU GPL 3](http://www.gnu.org/copyleft/gpl.html).

## Download and installation

### Windows

Windows binaries can be downloaded from GitHub:

- <https://github.com/ealbiter/qnotero/releases>

### Linux
Linux users can install Qnotero through the source code:

1. Download the latest version of the source code from <https://github.com/ealbiter/qnotero/releases>, and uncompress it.

2. Open a terminal and go to the folder where qnotero source code was uncompressed.

3. Run the following command:

```
      sudo python setup.py install
```

In Arch Linux and its derivatives, users can install Qnotero from AUR using yay, or other AUR helper:

```
      yay -S qnotero
```

### mac OS

mac OS users can download the compressed bundle, uncompress it and copy to the application folder.

### Other operating systems

For other operating systems, you can (try to) run Qnotero from source. Source code for stable releases can be downloaded from GitHub:

- <https://github.com/ealbiter/qnotero/releases>

## Dependencies

Qnotero has the following dependencies.

- [Python] -- As of Qnotero 1.0.0, Python >= 3.3 is required.
- [PyQt5] -- Pass `--qt4` as command-line argument for PyQt4 legacy support.

## Gnote integration (Linux only)

If you have Gnote installed (a note-taking program for Linux), Qnotero automatically searches Gnote for a (section in a) note belonging to a specific article. Qnotero expects each note to be preceded by a bold line containing at least the name of the first author and the year of publication within parentheses, like so:

    Duhamel et al. (1992) Science 255

[python]: https://www.python.org/
[PyQt5]: http://www.riverbankcomputing.co.uk/software/pyqt/download

[Overview]: #overview
[What is Qnotero?]: #what-is-qnotero
[Download and installation]: #download-and-installation
[Windows]: #windows
[Linux]: #linux
[mac OS]: #mac-os
[Other operating systems]: #other-operating-systems
[Dependencies]: #dependencies
[Gnote integration (Linux only)]: #gnote-integration-linux-only