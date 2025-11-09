# setup_directories.py
"""
Setup script to create necessary directories for the fixedpdb project.
"""

import os
import argparse
from pathlib import Path


def create_directory(path, description="directory"):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    print(f"✓ Created {description}: {path}")


def setup_project_structure(base_dir="."):
    """Set up the complete project directory structure."""

    base_path = Path(base_dir)

    # Main project directories
    directories = {
        "input_pdb": "Directory for original PDB files",
        "output_fixed": "Directory for fixed PDB files",
        "logs": "Directory for processing logs",
        "temp": "Directory for temporary files during processing",
    }

    print("Setting up fixedpdb project structure...")
    print("=" * 50)

    for dir_name, description in directories.items():
        dir_path = base_path / dir_name
        create_directory(dir_path, description)

    print("\n" + "=" * 50)
    print("Project structure setup complete!")
    print("\nDirectory structure:")
    print(f"├── {base_path}/input_pdb/     # Place your original PDB files here")
    print(f"├── {base_path}/output_fixed/  # Fixed PDB files will be saved here")
    print(f"├── {base_path}/logs/          # Processing logs")
    print(f"└── {base_path}/temp/          # Temporary processing files")


def main():
    parser = argparse.ArgumentParser(
        description="Setup directories for fixedpdb project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_directories.py                    # Setup in current directory
  python setup_directories.py --base-dir /path/to/project  # Setup in specific directory
        """,
    )

    parser.add_argument(
        "--base-dir",
        default=".",
        help="Base directory for project structure (default: current directory)",
    )

    parser.add_argument(
        "--force", action="store_true", help="Force creation even if directories exist"
    )

    args = parser.parse_args()

    # Validate base directory
    base_path = Path(args.base_dir)
    if not base_path.exists():
        print(f"Creating base directory: {base_path}")
        base_path.mkdir(parents=True, exist_ok=True)

    # Check if directories already exist and warn if --force is not used
    if not args.force:
        existing_dirs = []
        for dir_name in ["input_pdb", "output_fixed", "logs", "temp"]:
            if (base_path / dir_name).exists():
                existing_dirs.append(dir_name)

        if existing_dirs:
            print(f"Warning: The following directories already exist: {existing_dirs}")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != "y":
                print("Setup cancelled.")
                return

    setup_project_structure(args.base_dir)


if __name__ == "__main__":
    main()
