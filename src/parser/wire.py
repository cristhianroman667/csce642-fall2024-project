import csv

input_path = "/home/grads/c/chengjialiu/rl_proj/n50.nets"
output_path = "/home/grads/c/chengjialiu/rl_proj/n50_nets.csv"

# Read data
rows = []
current_row = []
net_count = 1

with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith("NetDegree"):
            # # if met new NetDegree, save the current row and start a new row
            # if current_row:
            #     rows.append(current_row)
            current_row = f"net{net_count}"
            net_count += 1
        elif line.startswith("sb") or line.startswith("p"):  
            blk_name = line.split()[0].strip()
            rows.append([current_row, blk_name])


# Save to CSV
with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Create header
    header = ["net", "blk"]
    writer.writerow(header)
    # Write data
    writer.writerows(rows)

print("Net data saved to", output_path)