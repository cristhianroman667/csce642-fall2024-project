import csv
import re

# Input data
input_path = "/home/grads/c/chengjialiu/rl_proj/n10.blocks"
output_path = "/home/grads/c/chengjialiu/rl_proj/n10_block.csv"

# Read data
rows = []
with open(input_path, "r") as file:
    for line in file:
        if line.startswith("sb"):
            parts = line.split(maxsplit=3)      # Split into 4 parts
            name = parts[0]                     # First part is the name
            vertex_data = parts[3]              # Fourth part is the vertex data
            
            # Extract vertices
            vertices = re.findall(r"\((\d+),\s*(\d+)\)", vertex_data)   # Find all pairs of integers
            if len(vertices) == 4:                                      
                vertices = [tuple(map(int, v)) for v in vertices]  
                rows.append([name] + vertices)

# Calculate dimensions and center
output_data = [["name", "w", "h", "x", "y"]]  # Header row
for row in rows:
    name = row[0]
    vertices = row[1:]
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    # w: width, h: height, x_center, y_center
    w = max(x_coords) - min(x_coords)
    h = max(y_coords) - min(y_coords)
    # center coordinates need to round down
    x_center = (max(x_coords) + min(x_coords)) // 2
    y_center = (max(y_coords) + min(y_coords)) // 2
    output_data.append([name, w, h, x_center, y_center])

# Save to CSV
with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_data)

print("Block data saved to", output_path)
