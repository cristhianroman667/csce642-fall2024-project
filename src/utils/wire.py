import csv

input_path = "/home/grads/c/chengjialiu/rl_proj/n300.nets"
output_path = "/home/grads/c/chengjialiu/rl_proj/n300_nets.csv"

# Read data
rows = []
current_row = []
net_count = 1

with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith("NetDegree"):
            # if met new NetDegree, save the current row and start a new row
            if current_row:
                rows.append(current_row)
            current_row = [f"net{net_count}"]
            net_count += 1
        # if the line is a block name
        elif line.startswith("sb") or line.startswith("p"):  
            blk_name = line.split()[0].strip()
            current_row.append(blk_name)
    
    # add the last row
    if current_row:
        rows.append(current_row)

# Save to CSV
with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Create header
    max_columns = max(len(row) for row in rows)
    header = ["name"] + [f"blk{i}" for i in range(1, max_columns)]
    writer.writerow(header)
    # Write data
    writer.writerows(rows)

print("Net data saved to", output_path)