from src.generator import generate_images
from src.utils import read_metadata, read_distribution

if __name__ == "__main__":
    distribution = read_distribution("distribution.json")
    metadata = read_metadata("metadata.json")
    generate_images(metadata, distribution)
