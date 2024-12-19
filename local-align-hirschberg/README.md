## Using the CLI Tool

If you run:
```
$ python3 space_local_align.py -h
```

You will get a nice little print out of exactly which options and command line arguments to specify to be able to search for a local alignment within our dataset at `../scrubbed-viral-data/scrubbed_sequences.csv`.

Can inspect the code to ensure that it really does work with Hirschberg and not local alignment directly! It's completely linear space.

## Output

The CLI tool outputs it's results in a neat JSON format, both human-readable and easily program-readable, ranked by top 10 results by default, unless the `-n` or `--count` switch was specified to the CLI.

See the sample output in `test_out1.json.sample` to get an idea of how your output will look like.

## Verification

There's a few ways to actually verify the output. Firstly, you can open up the `scrubbed_sequences.csv` file, find a substring of some genome and mess up a few characters. The CLI tool's output should return that genome as a top match. You can also go through the Jupyter Notebook and test your own input $\mathbf{v}$ with some reference $\mathbf{w}$ in the cell after the final function is defined, and compare this with a known working local alignment. There's likely other ways to verify the output, not listed here.