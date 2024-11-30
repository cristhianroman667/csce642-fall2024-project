import csv

# Input data
input_path = "/home/grads/c/chengjialiu/rl_proj/n300.pl"
output_path = "/home/grads/c/chengjialiu/rl_proj/n300_terminal.csv"

# Read data
rows = []
with open(input_path, "r") as file:
    for line in file:
        if line.startswith("p"):
            parts = line.split()
            name = parts[0]                     # First part is the name
            vertex_x_data = parts[1]            # Second part is the vertex x data
            vertex_y_data = parts[2]            # Third part is the vertex y data
            
            rows.append([name, vertex_x_data, vertex_y_data])

# Save to CSV
with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Create header
    header = ["name", "x", "y"]
    writer.writerow(header)
    writer.writerows(rows)

print("Terminal data saved to", output_path)
