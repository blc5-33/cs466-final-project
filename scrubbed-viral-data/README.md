From the proposal:
[NCBI Virus Dataset]{https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&SLen_i=1\%20TO\%20100000&HostLineage_ss=Homo\%20sapiens\%20(human),\%20taxid:9606&GenomeCompleteness_s=complete&Completeness_s=complete}

[NCBI Genome Dataset]{https://www.ncbi.nlm.nih.gov/datasets/genome/?taxon=10239}

## Data Scrubbing Methodology

Not all of the NCBI data for human coronviruses gave the complete sequences or genomes.
So in `../scrub_data.py` we filtered out the NCBI data such that we
only got complete sequences or genomes.