import argparse
from src.generator import Generator
from src.utils import read_metadata, read_distribution


def main(metadata_path, distribution_path):
    distribution = read_distribution(distribution_path)
    metadata = read_metadata(metadata_path)

    generator = Generator(metadata, distribution)
    generator.generate_images()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate images based on metadata and distribution."
    )
    parser.add_argument("metadata", type=str, help="Path to the metadata JSON file")
    parser.add_argument(
        "distribution", type=str, help="Path to the distribution JSON file"
    )

    args = parser.parse_args()
    main(args.metadata, args.distribution)
