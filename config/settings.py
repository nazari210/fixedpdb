# Configuration settings for the fixedpdb project

# Default directories
DEFAULT_INPUT_DIR = "./input_pdb"
DEFAULT_OUTPUT_DIR = "./output_fixed"

# Processing settings
MAX_WORKERS = None  # Use all available CPU cores
CHUNK_SIZE = 100  # Process files in chunks to manage memory

# File extensions
PDB_EXTENSION = ".pdb"
FIXED_EXTENSION = "_fixed.pdb"
