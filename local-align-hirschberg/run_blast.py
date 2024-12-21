import subprocess
import psutil
import time

command = [
    "../../../ncbi-blast-2.16.0+/bin/blastn",
    "-query", "ex_seq.fasta",
    "-db", "../scrubbed-viral-data/scrubbed_db",
    "-out", "blast_results.txt",
    "-outfmt", "6",
    "-word_size", "4",
]

proc = subprocess.Popen(command)

peak_memory = 0
start_time = time.time()

while True:
    if proc.poll() is not None:
        break
    try:
        p = psutil.Process(proc.pid)
        mem_info = p.memory_info()
        peak_memory = max(peak_memory, mem_info.rss)
    except psutil.NoSuchProcess:
        pass
    time.sleep(0.1)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"BLAST completed in {elapsed_time:.2f} seconds")
print(f"Peak memory usage: {peak_memory / (1024*1024):.2f} MB")