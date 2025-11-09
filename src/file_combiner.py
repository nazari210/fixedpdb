# src/file_combiner.py
import os
import re


def copy_cryst1_record(input_file, output_file):
    """Copy CRYST1 record from input to output file."""
    with open(input_file, "r") as pdb_in, open(output_file, "w") as pdb_out:
        for line in pdb_in:
            if line.startswith("CRYST1"):
                pdb_out.write(line)
                break


def merge_pdb_files(components, output_file):
    """Merge multiple PDB file components into a single output file."""
    with open(output_file, "w") as merged_file:
        for component_file in components:
            if os.path.exists(component_file):
                with open(component_file, "r") as f:
                    lines = f.readlines()
                    merged_file.writelines(lines)


def extract_openmm_date_from_header(header_file):
    """Extract OpenMM version and date from header file."""
    try:
        with open(header_file, "r") as f:
            for line in f:
                if "OPENMM" in line.upper():
                    # Look for lines containing OpenMM version information
                    if "OPENMM" in line and ("CREATED" in line or "GENERATED" in line):
                        # Extract the date part after OPENMM version
                        parts = line.split("OPENMM")
                        if len(parts) > 1:
                            # Get the part after OPENMM and look for date
                            after_openmm = parts[1]
                            # Look for date pattern like YYYY-MM-DD
                            date_match = re.search(r"\d{4}-\d{2}-\d{2}", after_openmm)
                            if date_match:
                                # Extract version number as well
                                version_match = re.search(r"(\d+\.\d+)", after_openmm)
                                version = (
                                    version_match.group(1) if version_match else "8.2"
                                )
                                return f"OPENMM {version}, {date_match.group()}"
    except FileNotFoundError:
        pass

    # Default fallback if no date found
    return "OPENMM 8.2, 2025-05-18"


def create_remark_file(output_file, openmm_version_line=None):
    """Create the standard REMARK file with proper OpenMM version."""
    if openmm_version_line is None:
        openmm_version_line = "OPENMM 8.2, 2025-05-18"

    with open(output_file, "w") as f:
        f.write("REMARK   1\n")
        f.write("REMARK   1 BY FIXEDPDB.COM\n")
        # Add the OpenMM version line from the header
        f.write(f"REMARK   1 CREATED WITH {openmm_version_line}\n")
