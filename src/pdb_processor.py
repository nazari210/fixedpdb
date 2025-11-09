# src/pdb_processor.py
from pdbfixer import PDBFixer
from openmm.app import PDBFile
import os


def process_pdb_file(pdb_file_path, output_prefix):
    """
    Process a single PDB file using PDBFixer.
    The output_prefix should include the temp directory path.
    Returns True if successful, False otherwise.
    """
    try:
        # Initialize PDBFixer
        fixer = PDBFixer(filename=pdb_file_path)
        fixer.findMissingResidues()

        # Handle missing residues at the terminal ends
        chains = list(fixer.topology.chains())
        keys = list(fixer.missingResidues.keys())
        for key in keys:
            chain = chains[key[0]]
            if key[1] == 0 or key[1] == len(list(chain.residues())):
                del fixer.missingResidues[key]

        # Replace nonstandard residues and add missing atoms
        fixer.findNonstandardResidues()
        fixer.replaceNonstandardResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()

        # Write output files to temp directory using the provided output_prefix
        model_file = f"{output_prefix}_model.pdb"
        header_file = f"{output_prefix}_header.pdb"
        footer_file = f"{output_prefix}_footer.pdb"

        with open(model_file, "w") as f:
            PDBFile.writeModel(fixer.topology, fixer.positions, f)
        with open(header_file, "w") as f:
            PDBFile.writeHeader(fixer.topology, f)
        with open(footer_file, "w") as f:
            PDBFile.writeFooter(fixer.topology, f)

        return True

    except Exception as e:
        print(f"Error processing {pdb_file_path}: {e}")
        return False
