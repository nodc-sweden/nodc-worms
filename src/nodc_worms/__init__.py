import functools
import sys
import pathlib
import importlib.resources

from .taxa_worms import TaxaWorms


TAXA_WORMS_FILE_PATH = importlib.resources.files("CONFIG_FILES") / "taxa_worms.txt"


@functools.cache
def get_taxa_worms_object() -> "TaxaWorms":
    return TaxaWorms(str(TAXA_WORMS_FILE_PATH))

