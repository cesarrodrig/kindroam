# KindRoam

[![Build Status](https://travis-ci.com/cesar0094/kindroam.svg?branch=master)](https://travis-ci.com/cesar0094/kindroam)

Export Kindle highlights to Roam, grouping them by books.

KindRoam exports Kindle highlights into Roam pages, grouping them by book
and writting them as Markdown files. It keeps track of the last time the
highlights were exported so only the newest ones are used.

When importing an already existing page, Roam appends the new data, so
KindRoam makes sure to only export highlights that have not been written
before.

The Markdown files are written to a folder and they can be directly
imported to Roam. Each book gets its own Roam page. After importing the
highlights, the files can be deleted manually or using the `clean`
command. It is recommended to import all generated Roam pages before
doing a new export because books with new highlights will be overwritten.


## Installation

To install the command-line tool, run:

```
pip install .
```

After this, `kindroam` is available as a CLI.

## Usage

To export highlights from a `My Clippings.txt` file, use the `export`
command. If you are using OSX and have your Kindle plugged in, you
can run:

```
kindroam export
```

Otherwise, you need to specify where the `My Clippings.txt` file is with
the `-f/--filename` option:

```
kindroam export -f "My Clippings.txt"
```
