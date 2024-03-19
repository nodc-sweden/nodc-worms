import functools
import sys
import pathlib
import importlib.resources

from .taxa_worms import TaxaWorms


# TAXA_WORMS_FILE_PATH = importlib.resources.files("src/nodc_worms/CONFIG_FILES") / "taxa_worms.txt"

if getattr(sys, 'frozen', False):
    THIS_DIR = pathlib.Path(sys.executable).parent
else:
    THIS_DIR = pathlib.Path(__file__).parent

TAXA_WORMS_FILE_PATH = THIS_DIR / "CONFIG_FILES" / "taxa_worms.txt"


@functools.cache
def get_taxa_worms_object() -> "TaxaWorms":

    return TaxaWorms(str(TAXA_WORMS_FILE_PATH))

