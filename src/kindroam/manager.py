import collections
import datetime
import json
import os
from typing import Dict, Iterator, List

from kindroam import highlight

HighlightType = highlight.Highlight
GroupedHighlights = Dict[str, List[HighlightType]]


class Manager:

    def __init__(self, db_filename: str, books_dir='books') -> None:
        self.__db_filename = db_filename
        self.__books_dir = books_dir
        self._load_db()

    def sync_highlights(self, highlights: List[HighlightType]) -> None:
        if not highlights:
            print("No highlights to sync.")
            return

        # Filtering highlights that were created after the last checkpoint.
        filtered_hls: Iterator[HighlightType] = filter(
            lambda c: c.added > self.db['last_updated'], highlights)

        books_dir = self.db['books_dir']
        highlights_by_book = group_by_book(filtered_hls)

        num_new_highlights = 0
        for book, highlights in highlights_by_book.items():

            book_filename = os.path.join(books_dir, f"{book}.md")
            with open(book_filename, 'w') as f:

                num_new_highlights += len(highlights)
                for c in highlights:
                    f.write(c.to_block())

                print(f"Exported {len(highlights)} highlights of {book}.")

        self.db['last_updated'] = datetime.datetime.now()
        self._save_db()
        print(f"Exported {num_new_highlights} new highlights.")

    def _load_db(self) -> None:

        if not os.path.isfile(self.__db_filename):
            self.db = {
                'last_updated': datetime.datetime(2000, 1, 1),
                'books_dir': self.__books_dir,
            }
            return

        with open(self.__db_filename, 'r') as f:
            self.db = json.load(f)
            assert 'last_updated' in self.db
            self.db['last_updated'] = datetime.datetime.fromisoformat(
                self.db['last_updated'])

    def _save_db(self) -> None:
        with open(self.__db_filename, 'w') as f:
            json.dump(self.db, f, default=str)


def group_by_book(
        highlights: Iterator[HighlightType]) -> Dict[str, List[HighlightType]]:
    by_book = collections.defaultdict(list)
    for clip in highlights:
        by_book[clip.book].append(clip)

    return by_book
