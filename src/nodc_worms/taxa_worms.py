import pathlib

import polars as pl


class TaxaWorms:
    def __init__(self, path: str | pathlib.Path, **kwargs):
        self._path = pathlib.Path(path)
        self._encoding = kwargs.get("encoding", "cp1252")

        self._header = []
        self._data = dict()
        self._synonyms = dict()

        self._load_file()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def source(self) -> str:
        return self.path.name

    @property
    def columns(self) -> list[str]:
        return sorted(self._df.columns)

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator="\t", encoding=self._encoding)

    def get_aphia_id(self, scientific_name: str) -> str:
        result = self._df.filter(pl.col("scientific_name") == scientific_name)["aphia_id"]
        if not len(result):
            return ""
        if len(result) > 1:
            raise ValueError(
                f"Scientific name matches several AphiaID: {scientific_name}"
            )
        return result[0]
