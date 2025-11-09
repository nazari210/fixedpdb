# src/sheet_fixer.py
def process_sheet_records(input_file, output_file, chain_info):
    """Process SHEET records, modify residue numbers based on chain info."""
    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        for line in f_in:
            # Check if the line starts with "SHEET"
            if line.startswith("SHEET"):
                # Extract initial and terminal chain identifiers and residue numbers
                init_chain_id = line[21]  # Initial chain identifier (column 22)
                end_chain_id = line[32]  # Terminal chain identifier (column 33)
                init_residue_num = int(
                    line[22:26].strip()
                )  # Initial residue sequence number (columns 23-26)
                end_residue_num = int(
                    line[33:37].strip()
                )  # Terminal residue sequence number (columns 34-37)

                # Modify the initial residue number if the chain ID matches
                if init_chain_id in chain_info:
                    addnum = chain_info[init_chain_id] - 1
                    new_init_residue_num = init_residue_num - addnum
                else:
                    new_init_residue_num = init_residue_num

                # Modify the terminal residue number if the chain ID matches
                if end_chain_id in chain_info:
                    addnum = chain_info[end_chain_id] - 1
                    new_end_residue_num = end_residue_num - addnum
                else:
                    new_end_residue_num = end_residue_num

                # Extract current strand registration fields
                cur_chain_id = line[49]  # Current chain identifier (column 50)
                cur_res_seq_str = line[
                    50:54
                ].strip()  # Current residue sequence number (columns 51-54)

                # Handle blank or empty residue numbers
                if cur_res_seq_str.isdigit():
                    cur_res_seq = int(cur_res_seq_str)
                    if cur_chain_id in chain_info:
                        addnum = chain_info[cur_chain_id] - 1
                        new_cur_res_seq = cur_res_seq - addnum
                    else:
                        new_cur_res_seq = cur_res_seq
                else:
                    # Leave blank fields unchanged
                    new_cur_res_seq = cur_res_seq_str

                # Extract previous strand registration fields
                prev_chain_id = line[64]  # Previous chain identifier (column 65)
                prev_res_seq_str = line[
                    65:69
                ].strip()  # Previous residue sequence number (columns 66-69)

                # Handle blank or empty residue numbers
                if prev_res_seq_str.isdigit():
                    prev_res_seq = int(prev_res_seq_str)
                    if prev_chain_id in chain_info:
                        addnum = chain_info[prev_chain_id] - 1
                        new_prev_res_seq = prev_res_seq - addnum
                    else:
                        new_prev_res_seq = prev_res_seq
                else:
                    # Leave blank fields unchanged
                    new_prev_res_seq = prev_res_seq_str

                # Construct the modified SHEET line
                new_line = (
                    f"{line[:22]}{new_init_residue_num:4d}{line[26:33]}"
                    f"{new_end_residue_num:4d}{line[37:50]}"
                    f"{str(new_cur_res_seq).rjust(4)}{line[54:65]}"
                    f"{str(new_prev_res_seq).rjust(4)}{line[69:]}"
                )
                f_out.write(new_line)  # Write the modified SHEET line
            # Only keep SHEET lines, ignore all other lines
