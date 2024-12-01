import csv

with open("scrubbed-viral-data/sequences.fasta", "r") as file:
    fasta_lines = file.readlines()

sequences = []
current_sequence = ""
current_description = ""

for line in fasta_lines:
    if line.startswith(">"):
        if current_description and current_sequence:
            sequences.append((current_description, current_sequence))
        current_description = line.strip()[1:]
        current_sequence = ""
    else:
        current_sequence += line.strip()

if current_description and current_sequence:
    sequences.append((current_description, current_sequence))

filtered_sequences = [
    (desc, seq) for desc, seq in sequences if "complete sequence" in desc or "complete genome" in desc
]

with open("scrubbed-viral-data/scrubbed_sequences.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Description", "Sequence"])  # Write header
    for description, sequence in filtered_sequences:
        csv_writer.writerow([description, sequence])
