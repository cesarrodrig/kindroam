import datetime
import io
import re
from typing import IO, List


class Highlight(object):

    def __init__(self,
                 book: str,
                 author: str,
                 content: str,
                 added: datetime.datetime,
                 note: str = ""):

        self.book = book
        self.author = author
        self.content = content
        self.added = added
        self.note = note

    def to_block(self):
        block = f"- {self.content}\n"
        if self.note != "":
            block += f"\t- {self.note}\n"
        return block


def load_highlights(filename: str) -> List[Highlight]:
    with io.open(filename, mode='rb') as f:
        return parse_highlights(f)


def parse_highlights(f: IO) -> List[Highlight]:

    content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')

    # Ignore the last lines because it is blank
    lines = content.split('\r\n')[:-1]

    assert len(lines) % 5 == 0
    highlights = []
    highlight = None

    # Every 5 lines, there is a different highlight
    for i in range(0, len(lines), 5):

        # Parse added as a timestamp
        info = lines[i + 1]
        added = info.split(" | Added on ")[-1].strip()
        added = datetime.datetime.strptime(added.strip(),
                                           "%A, %B %d, %Y %I:%M:%S %p")

        # Parse book and author line
        book_and_author = lines[i].strip()
        results = re.search(r"\(.*\)", book_and_author)
        if not results:
            raise RuntimeError("No Author Found")

        author_start = results.start()
        book = book_and_author[:author_start].strip()
        author = book_and_author[author_start:].lstrip("(").rstrip(")")

        # The content is in one line fortunately
        content = lines[i + 3].strip()

        # A + at the beginning indicates to be a note that should be attached
        # to the previous highlight.
        if content.startswith("+") and highlight is not None:
            highlight.note = content[1:]
            continue

        highlight = Highlight(book, author, content, added)
        highlights.append(highlight)

    return highlights
