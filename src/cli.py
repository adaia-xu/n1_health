import click
from pipeline import run_pipeline

@click.command()
@click.option("--input", "xml_path", default="data/raw/export.xml", help="Path to Apple Health export.xml")
def main(xml_path):
    """Run the N1-Health pipeline on an Apple Health export."""
    run_pipeline(xml_path)

if __name__ == "__main__":
    main()