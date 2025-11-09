# batch_process.py
import os
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.pdb_processor import process_pdb_file
from src.helix_fixer import process_helix_records
from src.sheet_fixer import process_sheet_records
from src.utils import get_pdb_ids_from_directory, get_chain_info
from src.file_combiner import (
    copy_cryst1_record,
    merge_pdb_files,
    create_remark_file,
)


def process_single_pdb(pdb_id, input_dir, output_dir, temp_dir, logs_dir):
    """Process a single PDB file through the complete pipeline."""
    try:
        input_pdb_path = os.path.join(input_dir, f"{pdb_id}.pdb")

        # Step 1: Process with PDBFixer - save temp files in temp directory
        pdbfixer_output_prefix = os.path.join(temp_dir, pdb_id)
        success = process_pdb_file(input_pdb_path, pdbfixer_output_prefix)
        if not success:
            return pdb_id, "error"

        # Step 2: Get chain info for this specific PDB
        chain_info = get_chain_info(input_pdb_path)

        # Step 3: Process HELIX records - save in temp directory
        helix_file = os.path.join(temp_dir, f"{pdb_id}helix.pdb")
        process_helix_records(input_pdb_path, helix_file, chain_info)

        # Step 4: Process SHEET records - save in temp directory
        sheet_file = os.path.join(temp_dir, f"{pdb_id}sheet.pdb")
        process_sheet_records(input_pdb_path, sheet_file, chain_info)

        # Step 5: Create standard REMARK file with OpenMM date from header
        # Get OpenMM date from the PDBFixer header file
        header_file = os.path.join(temp_dir, f"{pdb_id}_header.pdb")
        openmm_date = extract_openmm_date_from_header(header_file)
        standard_remark_file = os.path.join(temp_dir, "remark.pdb")
        create_remark_file(standard_remark_file, openmm_date)

        # Step 7: Copy CRYST1 record from the PDBFixer header file
        cryst_file = os.path.join(temp_dir, f"{pdb_id}crystm.pdb")
        copy_cryst1_record(header_file, cryst_file)

        # Step 8: Merge all components in the exact order from your workflow
        components = [
            standard_remark_file,  # Standard fixedpdb REMARK (first)
            helix_file,  # HELIX records (only corrected HELIX lines)
            sheet_file,  # SHEET records (only corrected SHEET lines)
            cryst_file,  # CRYST1 record
            os.path.join(
                temp_dir, f"{pdb_id}_model.pdb"
            ),  # ATOM/HETATM records from temp
            os.path.join(
                temp_dir, f"{pdb_id}_footer.pdb"
            ),  # Footer records like END, TER, CONECT from temp
        ]

        # Final output file in the main output directory
        final_file = os.path.join(output_dir, f"{pdb_id}_fixed.pdb")
        merge_pdb_files(components, final_file)

        return pdb_id, "success"

    except Exception as e:
        print(f"Error processing {pdb_id}: {e}")
        return pdb_id, "error"


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
                            import re

                            date_match = re.search(r"\d{4}-\d{2}-\d{2}", after_openmm)
                            if date_match:
                                return f"OPENMM 8.2, {date_match.group()}"
    except FileNotFoundError:
        pass

    # Default fallback if no date found
    return "OPENMM 8.2, 0000-00-00"


def main():
    parser = argparse.ArgumentParser(description="Process PDB files in batch")
    parser.add_argument(
        "--input-dir", required=True, help="Directory containing input PDB files"
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory for output files"
    )
    parser.add_argument(
        "--temp-dir",
        default="temp",
        help="Directory for temporary files (default: temp)",
    )
    parser.add_argument(
        "--logs-dir", default="logs", help="Directory for log files (default: logs)"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=None,
        help="Maximum number of parallel workers",
    )

    args = parser.parse_args()

    # Create directories if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.temp_dir, exist_ok=True)
    os.makedirs(args.logs_dir, exist_ok=True)

    # Get PDB IDs from input directory (no CSV needed)
    pdb_ids = get_pdb_ids_from_directory(args.input_dir)
    print(f"Found {len(pdb_ids)} PDB files to process")

    # Process PDB files in parallel
    results = []
    max_workers = args.max_workers or os.cpu_count() or 4

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdb = {
            executor.submit(
                process_single_pdb,
                pdb_id,
                args.input_dir,
                args.output_dir,
                args.temp_dir,
                args.logs_dir,
            ): pdb_id
            for pdb_id in pdb_ids
        }

        for future in as_completed(future_to_pdb):
            pdb_id, status = future.result()
            results.append((pdb_id, status))
            print(f"Processed {pdb_id}: {status}")

    # Save results to a log file in logs directory
    log_file_path = os.path.join(args.logs_dir, "processing_log.txt")
    with open(log_file_path, "w") as log_file:
        for pdb_id, status in results:
            log_file.write(f"{pdb_id}: {status}\n")

    print("Processing complete.")


if __name__ == "__main__":
    main()
