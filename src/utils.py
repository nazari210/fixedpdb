# src/utils.py
import os
import re


def get_pdb_ids_from_directory(folder_path):
    """Extract PDB IDs from .pdb files in a directory without saving to CSV."""
    pdb_ids = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdb"):
            # Extract PDB ID from filename (without extension)
            pdb_id = os.path.splitext(filename)[0].lower()
            pdb_ids.append(pdb_id)
    return pdb_ids


def get_chain_info(pdb_file):
    """Extract chain information and calculate addnum for each chain."""
    chain_info = {}

    with open(pdb_file, "r") as file:
        for line in file:
            if line.startswith("ATOM"):
                chain_id = line[21]
                residue_seq = int(line[22:26].strip())

                if chain_id not in chain_info:
                    chain_info[chain_id] = residue_seq

    return chain_info


def extract_cryst1_record(input_file, output_file):
    """Copy CRYST1 record from input to output file."""
    with open(input_file, "r") as pdb_in, open(output_file, "w") as pdb_out:
        for line in pdb_in:
            if line.startswith("CRYST1"):
                pdb_out.write(line)
                break


def extract_remark_record(input_file, output_file):
    """Copy REMARK record from input to output file."""
    with open(input_file, "r") as pdb_in, open(output_file, "w") as pdb_out:
        for line in pdb_in:
            if line.startswith("REMARK"):
                pdb_out.write(line)
                break


# Add new functions from your workflow
def extract_chain_info_from_directory(input_dir):
    """Extract chain info for all PDB files in directory."""
    chain_info_dict = {}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdb"):
            pdb_id = os.path.splitext(filename)[0]
            pdb_file = os.path.join(input_dir, filename)
            chain_info_dict[pdb_id] = get_chain_info(pdb_file)
    return chain_info_dict
