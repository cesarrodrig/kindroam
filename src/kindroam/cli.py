import glob
import os

import click

from kindroam.highlight import load_highlights
from kindroam.manager import Manager

KINDROAM_DB_FILENAME = os.environ.get('KINDROAM_DB_FILENAME', ".kindroam.json")
KINDROAM_CLIPPINGS_FILE = '/Volumes/Kindle/documents/My Clippings.txt'
KINDROAM_BOOK_DIR = 'books'


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """
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

    For usage information, see help for the `export` and `clean` commands.
    """
    pass


@cli.command()
@click.option('--books-dir',
              default=KINDROAM_BOOK_DIR,
              help="Directory where the Roam Pages are saved.")
def clean(books_dir):
    """Delete all Markdown files (.md) from the books directory."""
    for filename in glob.glob(os.path.join(books_dir, '*.md')):
        os.remove(filename)


@cli.command()
@click.option('-f',
              '--filename',
              default=KINDROAM_CLIPPINGS_FILE,
              show_default=True,
              help="Location of 'My Clippings.txt'.")
@click.option('--books-dir',
              default=KINDROAM_BOOK_DIR,
              help="Directory where the Roam Pages are saved.")
def export(filename, books_dir):
    """Load highlights from a `My Clippings.txt` file and export them
    as Roam pages to the books directory.

    By default, the produced Markdown files are written to the folder
    `books` in this project. To choose another directory, use `--books-dir`.
    The specified directory will be saved for future runs.

    A separate Mardown file is created for each book with its highlights
    inside. The name of the file is the name of the book. Highlights are
    separated into individual blocks.
    """

    # Making sure the books folder exists
    try:
        os.mkdir(books_dir)
    except FileExistsError:
        pass

    manager = Manager(KINDROAM_DB_FILENAME, books_dir)
    highlights = load_highlights(filename)
    manager.sync_highlights(highlights)


if __name__ == '__main__':
    cli()
