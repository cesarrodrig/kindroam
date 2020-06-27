import collections
from dataclasses import dataclass
import datetime
import json
import os
from typing import Dict, Iterator, List

from kindroam import highlight

HighlightType = highlight.Highlight
GroupedHighlights = Dict[str, List[HighlightType]]


@dataclass
class DB:
    filename: str
    books_dir: str
    last_updated: datetime.datetime

    @classmethod
    def load(cls, filename: str, books_dir: str) -> 'DB':

        if not os.path.isfile(filename):
            return DB(filename=filename,
                      last_updated=datetime.datetime(2000, 1, 1),
                      books_dir=books_dir)

        with open(filename, 'r') as f:

            db_json = json.load(f)
            assert 'last_updated' in db_json
            last_updated = datetime.datetime.fromisoformat(
                db_json['last_updated'])

            return cls(filename=filename,
                       last_updated=last_updated,
                       books_dir=db_json['books_dir'])

    def save(self) -> None:
        db_json = {
            'last_updated': self.last_updated,
            'books_dir': self.books_dir,
        }
        with open(self.filename, 'w') as f:
            json.dump(db_json, f, default=str)


class Manager:

    def __init__(self, db_filename: str, books_dir: str = 'books') -> None:
        self.db = DB.load(db_filename, books_dir)

    def sync_highlights(self, highlights: List[HighlightType]) -> None:
        if not highlights:
            print("No highlights to sync.")
            return

        # Filtering highlights that were created after the last checkpoint.
        filtered_hls: Iterator[HighlightType] = filter(
            lambda c: c.added > self.db.last_updated, highlights)

        highlights_by_book = group_by_book(filtered_hls)

        num_new_highlights = 0
        exported_prints = []
        for book, highlights in highlights_by_book.items():

            book_filename = os.path.join(self.db.books_dir, f"{book}.md")
            if os.path.isfile(book_filename):
                self._warn_book_exists(book)

            with open(book_filename, 'w') as f:

                num_new_highlights += len(highlights)
                for c in highlights:
                    f.write(c.to_block())

                exported_prints.append(
                    f"Exported {len(highlights)} highlights of {book}.")

        for p in exported_prints:
            print(p)

        self.db.last_updated = datetime.datetime.now()
        self.db.save()
        print(f"Exported {num_new_highlights} new highlights.")

    def _warn_book_exists(self, book: str):
        prompt = f"'{book}' has new highlights but the file already exists. "
        prompt += "Make sure it has alaready been imported into Roam before "
        prompt += "proceeding. This action will overwrite the existing file.\n"
        prompt += "\n> Press Enter to continue\n"
        input(prompt)


def group_by_book(
        highlights: Iterator[HighlightType]) -> Dict[str, List[HighlightType]]:
    by_book = collections.defaultdict(list)
    for clip in highlights:
        by_book[clip.book].append(clip)

    return by_book
