# fixedpdb

A Python-based tool for batch processing and fixing PDB files using PDBFixer with enhanced HELIX and SHEET record correction.

## Overview

The `fixedpdb` project processes PDB files to fix common structural issues using PDBFixer, with additional corrections for HELIX and SHEET records that maintain proper residue numbering across different chain starting points. This tool is designed for batch processing of multiple PDB files with parallel execution capabilities. A databse of thousands fixed PDB structures by this tool is available at [fixedpdb.com](https://fixedpdb.com).

## Features

- **Batch Processing**: Process multiple PDB files simultaneously using parallel processing
- **PDBFixer Integration**: Uses PDBFixer to fix missing atoms, residues, and non-standard residues
- **HELIX and SHEET Record Correction**: Adjusts HELIX and SHEET record residue numbers based on chain information
- **Standard REMARK Generation**: Creates standardized REMARK records with OpenMM version information
- **CRYST1 Preservation**: Maintains crystallographic information in the output files
- **Temporary File Management**: Organizes temporary files during processing
- **Processing Logs**: Generates logs for tracking successful and failed file processing

## Installation

### Prerequisites

- Python 3.7 or higher
- Conda package manager

### Dependencies

First, install PDBFixer using conda:

```bash
conda install -c conda-forge pdbfixer
```


## Project Structure

```
├── batch_process.py         # Main script for batch processing
├── setup_directories.py     # Script to create required directories
├── README.md               # This file
├── config                  # Configuration files
└── src/                    # Source code directory
    ├── pdb_processor.py    # PDBFixer processing functions
    ├── helix_fixer.py      # HELIX record processing
    ├── sheet_fixer.py      # SHEET record processing
    ├── utils.py           # Utility functions
    └── file_combiner.py   # File merging functions
```

## Setup

1. Create the required directory structure:

```bash
python setup_directories.py
```

This creates:
- `input_pdb/` - Directory for original PDB files
- `output_fixed/` - Directory for fixed PDB files
- `logs/` - Directory for processing logs
- `temp/` - Directory for temporary files during processing

2. Place your PDB files in the `input_pdb/` directory

## Usage

Run the batch processing script:

```bash
python batch_process.py --input-dir input_pdb --output-dir output_fixed
```

### Command Line Options

- `--input-dir`: Directory containing input PDB files (required)
- `--output-dir`: Directory for output files (required)
- `--temp-dir`: Directory for temporary files (default: temp)
- `--logs-dir`: Directory for log files (default: logs)
- `--max-workers`: Maximum number of parallel workers (default: number of CPU cores)

### Example Usage

```bash
# Basic usage with default settings
python batch_process.py --input-dir input_pdb --output-dir output_fixed

# Custom directories and limited parallel processing
python batch_process.py --input-dir my_pdbs --output-dir fixed_pdbs --max-workers 4
```

## Processing Pipeline

The pipeline processes each PDB file through the following steps:

1. **PDBFixer Processing**: Fixes missing atoms, residues, and non-standard residues
2. **HELIX Record Correction**: Adjusts HELIX record residue numbers based on chain information
3. **SHEET Record Correction**: Adjusts SHEET record residue numbers based on chain information
4. **REMARK Generation**: Creates standardized REMARK records
5. **CRYST1 Preservation**: Maintains crystallographic information
6. **File Merging**: Combines all components in the correct order

## Output

- Fixed PDB files are saved in the output directory with `_fixed.pdb` suffix
- Processing logs are saved in the logs directory
- Temporary files are stored in the temp directory during processing

## Contributing

This project is hosted on GitHub at https://github.com/nazari210. Contributions are welcome!

## Contact

For questions or issues, please open an issue on the GitHub repository.
