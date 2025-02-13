import functools
import logging
import os
import pathlib

from nodc_worms.taxa_worms import TaxaWorms
from nodc_worms.translate_worms import TranslateDyntaxa

logger = logging.getLogger(__name__)

CONFIG_ENV = 'NODC_CONFIG'

CONFIG_FILE_NAMES = [
    'taxa_worms.txt',
    'translate_to_worms.txt',
]


CONFIG_DIRECTORY = None
if os.getenv(CONFIG_ENV) and pathlib.Path(os.getenv(CONFIG_ENV)).exists():
    CONFIG_DIRECTORY = pathlib.Path(os.getenv(CONFIG_ENV))

def get_config_path(name: str = None) -> pathlib.Path:
    if not CONFIG_DIRECTORY:
        raise NotADirectoryError(f'Config directory not found. Environment path {CONFIG_ENV} does not seem to be set.')
    if not name:
        return CONFIG_DIRECTORY
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    path = CONFIG_DIRECTORY / name
    if not path.exists():
        raise FileNotFoundError(f'Could not find config file {name}')
    return path



@functools.cache
def get_taxa_worms_object() -> "TaxaWorms":
    taxa_worms_config_path = get_config_path("taxa_worms.txt")
    return TaxaWorms(str(taxa_worms_config_path))


@functools.cache
def get_translate_worms_object() -> "TranslateDyntaxa":
    taxa_worms_config_path = get_config_path("translate_to_worms.txt")
    return TranslateDyntaxa(str(taxa_worms_config_path))


if __name__ == '__main__':
    taxa = get_taxa_worms_object()
    trans = get_translate_worms_object()