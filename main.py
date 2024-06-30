from src.generator import Generator
from src.utils import read_metadata, read_distribution

if __name__ == "__main__":
    distribution = read_distribution("distribution.json")
    metadata = read_metadata("metadata.json")

    generator = Generator(metadata, distribution)
    generator.generate_images()
