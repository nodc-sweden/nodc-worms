import functools
import pathlib

from nodc_config import Config

from nodc_worms.taxa_worms import TaxaWorms
from nodc_worms.translate_worms import TranslateDyntaxa


def get_config_path(nodc_conf: Config, name: str) -> pathlib.Path:
    path = nodc_conf.get_path(name)
    if path is None:
        raise FileNotFoundError(f"nodc-config path '{name}' not found")
    return path


@functools.cache
def get_taxa_worms_object(nodc_conf: Config) -> TaxaWorms:
    taxa_worms_config_path = get_config_path(nodc_conf, "taxa_worms.txt")
    return TaxaWorms(str(taxa_worms_config_path))


@functools.cache
def get_translate_worms_object(nodc_conf: Config) -> TranslateDyntaxa:
    taxa_worms_config_path = get_config_path(nodc_conf, "translate_to_worms.txt")
    return TranslateDyntaxa(str(taxa_worms_config_path))
