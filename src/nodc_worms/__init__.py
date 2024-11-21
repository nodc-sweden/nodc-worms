import functools
import logging
import os
import pathlib
import ssl

import requests
from nodc_worms.taxa_worms import TaxaWorms
from nodc_worms.translate_worms import TranslateDyntaxa

logger = logging.getLogger(__name__)

CONFIG_SUBDIRECTORY = 'nodc_worms'
CONFIG_FILE_NAMES = [
    'taxa_worms.txt',
    'translate_to_worms.txt',
]


CONFIG_DIRECTORY = None
if os.getenv('NODC_CONFIG'):
    CONFIG_DIRECTORY = pathlib.Path(os.getenv('NODC_CONFIG')) / CONFIG_SUBDIRECTORY
TEMP_CONFIG_DIRECTORY = pathlib.Path.home() / 'temp_nodc_config' / CONFIG_SUBDIRECTORY


CONFIG_URL = r'https://raw.githubusercontent.com/nodc-sweden/nodc_config/refs/heads/main/' + f'{CONFIG_SUBDIRECTORY}/'


def get_config_path(name: str) -> pathlib.Path:
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    if CONFIG_DIRECTORY:
        path = CONFIG_DIRECTORY / name
        if path.exists():
            return path
    temp_path = TEMP_CONFIG_DIRECTORY / name
    if temp_path.exists():
        return temp_path
    update_config_file(temp_path)
    if temp_path.exists():
        return temp_path
    raise FileNotFoundError(f'Could not find config file {name}')


def update_config_file(path: pathlib.Path) -> None:
    path.parent.mkdir(exist_ok=True, parents=True)
    url = CONFIG_URL + path.name
    try:
        res = requests.get(url, verify=ssl.CERT_NONE)
        with open(path, 'w', encoding='utf8') as fid:
            fid.write(res.text)
            logger.info(f'Config file "{path.name}" updated from {url}')
    except requests.exceptions.ConnectionError:
        logger.warning(f'Connection error. Could not update config file {path.name}')
        raise


def update_config_files() -> None:
    """Downloads config files from github"""
    for name in CONFIG_FILE_NAMES:
        target_path = TEMP_CONFIG_DIRECTORY / name
        update_config_file(target_path)


@functools.cache
def get_taxa_worms_object() -> "TaxaWorms":
    taxa_worms_config_path = get_config_path("taxa_worms.txt")
    return TaxaWorms(str(taxa_worms_config_path))


@functools.cache
def get_translate_worms_object() -> "TranslateDyntaxa":
    taxa_worms_config_path = get_config_path("translate_to_worms.txt")
    return TranslateDyntaxa(str(taxa_worms_config_path))


if __name__ == '__main__':
    update_config_files()