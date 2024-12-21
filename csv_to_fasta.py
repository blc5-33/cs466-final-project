import csv

input_csv = "scrubbed-viral-data/scrubbed_sequences.csv"
output_fasta = "scrubbed-viral-data/scrubbed_sequences.fasta"

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    with open(output_fasta, 'w', encoding='utf-8') as fastafile:
        for row in reader:
            description = row["Description"].strip('"')
            sequence = row["Sequence"].strip()
            
            fastafile.write(f">{description}\n")
            fastafile.write(f"{sequence}\n")