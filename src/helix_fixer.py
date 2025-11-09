# src/helix_fixer.py
def process_helix_records(input_file, output_file, chain_info):
    """Process HELIX records, modify residue numbers based on chain info."""
    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        for line in f_in:
            # Check if the line starts with "HELIX"
            if line.startswith("HELIX"):
                # Extract the chain identifier (column 32), starting residue (columns 22-25), and ending residue (columns 34-37)
                chain_id = line[31]  # Chain identifier in HELIX record
                start_residue = int(line[21:25])  # Starting residue sequence number
                end_residue = int(line[33:37])  # Ending residue sequence number

                # Check if the chain identifier matches one in chain_info
                if chain_id in chain_info:
                    addnum = chain_info[chain_id] - 1  # Calculate addnum for this chain

                    # Modify the starting and ending residue numbers
                    new_start_residue = start_residue - addnum
                    new_end_residue = end_residue - addnum

                    # Convert the modified residue numbers back to PDB format
                    new_line = (
                        f"{line[:21]}{new_start_residue:4d}{line[25:33]}"
                        f"{new_end_residue:4d}{line[37:]}"
                    )
                    f_out.write(new_line)  # Write the modified HELIX line
                else:
                    # Write the unmodified HELIX line if the chain ID does not match
                    f_out.write(line)
            # Only keep HELIX lines, ignore all other lines
