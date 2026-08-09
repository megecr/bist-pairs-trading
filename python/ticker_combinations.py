import csv
import os
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.abspath(os.path.join(script_dir, "..", "data"))

output_csv_path = os.path.join(folder_path, "paired_stocks.csv")

file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

with open(output_csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Stock1","Stock2"])

    for combo in combinations(file_names, 2):
        writer.writerow(combo)

print(f"Succesfully saved pairs to: {output_csv_path}")