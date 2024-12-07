## Using the CLI Tool

If you run:
```
$ python3 space_local_align.py -h
```

You will get a nice little print out of exactly which options and command line arguments to specify to be able to search for a local alignment within our dataset at `../scrubbed-viral-data/scrubbed_sequences.csv`.

Can inspect the code to ensure that it really does work with Hirschberg and not local alignment directly! It's completely linear space.

## Output

The CLI tool outputs it's results in a neat JSON format, both human-readable and easily program-readable, ranked by top 10 results by default, unless the `-n` or `--count` switch was specified to the CLI.