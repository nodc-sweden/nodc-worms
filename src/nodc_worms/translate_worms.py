import logging
import pathlib

import polars as pl

logger = logging.getLogger(__name__)


class TranslateDyntaxa:

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator='\t', encoding='utf8')

    def get(self, name: str) -> str | bool:
        """Returns the translated taxon name of the given name"""
        try:
            return self._df.row(by_predicate=(pl.col('scientific_name_from') == name), named=True)['scientific_name_to']
        except pl.exceptions.NoRowsReturnedError:
            return ''
