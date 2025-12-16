import logging
import pathlib

import polars as pl

logger = logging.getLogger(__name__)


class TranslateDyntaxa:
    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def source(self) -> str:
        return self.path.name

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator="\t", encoding="cp1252")

    def get(self, name: str) -> str | bool:
        """Returns the translated taxon name of the given name"""
        try:
            return self._df.row(
                by_predicate=(pl.col("scientific_name_from") == name), named=True
            )["scientific_name_to"]
        except pl.exceptions.NoRowsReturnedError:
            return ""

    def get_from_to_mapper(self):
        mapping = {}
        for item in self._df.to_dicts():
            mapping[item["scientific_name_from"]] = item["scientific_name_to"]
        return mapping
