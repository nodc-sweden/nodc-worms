import functools
import logging
import pathlib

import requests
from nodc_worms.taxa_worms import TaxaWorms
from nodc_worms.translate_worms import TranslateDyntaxa

logger = logging.getLogger(__name__)

THIS_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = THIS_DIR / "CONFIG_FILES"

CONFIG_URLS = [
    r'https://raw.githubusercontent.com/nodc-sweden/nodc-worms/main/src/nodc_worms/CONFIG_FILES/taxa_worms.txt',
    r'https://raw.githubusercontent.com/nodc-sweden/nodc-worms/main/src/nodc_worms/CONFIG_FILES/translate_to_worms.txt',
]


@functools.cache
def get_taxa_worms_object() -> "TaxaWorms":
    taxa_worms_config_path = CONFIG_DIR / "taxa_worms.txt"
    return TaxaWorms(str(taxa_worms_config_path))


@functools.cache
def get_translate_worms_object() -> "TranslateDyntaxa":
    taxa_worms_config_path = CONFIG_DIR / "translate_to_worms.txt"
    return TranslateDyntaxa(str(taxa_worms_config_path))


def update_config_files() -> None:
    """Downloads config files from github"""
    try:
        for url in CONFIG_URLS:
            name = pathlib.Path(url).name
            target_path = CONFIG_DIR / name
            res = requests.get(url)
            with open(target_path, 'w', encoding='utf8') as fid:
                fid.write(res.text)
                logger.info(f'Config file "{name}" updated from {url}')
    except requests.exceptions.ConnectionError:
        logger.warning('Connection error. Could not update config files!')

