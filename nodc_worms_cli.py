import typer

from nodc_worms import get_taxa_worms_object


def main(scientific_name:str):
    obj = get_taxa_worms_object()
    print(obj.get_aphia_id(scientific_name))


if __name__ == "__main__":
    typer.run(main)
