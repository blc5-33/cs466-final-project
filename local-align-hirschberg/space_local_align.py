import pandas as pd
import numpy as np
import argparse
import json
import time
import psutil
import os

from tqdm import tqdm


def delta(v_i, w_j):
    if v_i == w_j:
        return 1
    else:
        return -1


def find_windows(v: str, w: str):
    n = len(v)
    m = len(w)
    prev = [(0, -1, -1) for _ in range(n + 1)]  # (score, i, j) i and j of origin of score
    cur = [(0, -1, -1) for _ in range(n + 1)]
    max_score = 0
    windows = []

    for j_end in range(m + 1):
        for i_end in range(n + 1):
            new_score, i_beg, j_beg = 0, i_end, j_end  # origin is itself by default
            if i_end > 0:
                from_score, from_i_beg, from_j_beg = cur[i_end - 1]
                deletion_score = from_score - 1
                if deletion_score > new_score:
                    # inherit origins from previous cell
                    new_score, i_beg, j_beg = deletion_score, from_i_beg, from_j_beg
            if j_end > 0:
                from_score, from_i_beg, from_j_beg = prev[i_end]
                insertion_score = from_score - 1
                if insertion_score > new_score:
                    new_score, i_beg, j_beg = insertion_score, from_i_beg, from_j_beg
            if i_end > 0 and j_end > 0:
                from_score, from_i_beg, from_j_beg = prev[i_end - 1]
                match_score = from_score + delta(v[i_end - 1], w[j_end - 1])
                if match_score > new_score:
                    new_score, i_beg, j_beg = match_score, from_i_beg, from_j_beg

            cur[i_end] = (new_score, i_beg, j_beg)
            if new_score > max_score:
                max_score = new_score
                # print(f'new window of score {max_score}')
                # window index is 0-indexed for string access, but sequence index is 1-indexed
                windows = [(i_beg, j_beg, i_end, j_end)]
            elif new_score == max_score and max_score > 0:
                # print(f'continuing window of score {max_score}')
                windows.append((i_beg, j_beg, i_end, j_end))

        prev = cur
        cur = [(0, -1, -1) for _ in range(n + 1)]
        # print([p[0] for p in prev])

    # print([c[0] for c in cur])
    return max_score, windows


# Returns score of last col only, not alignment string
def needleman_wunsch_score(v: str, w: str):
    n = len(v)
    m = len(w)
    prev = np.zeros(n + 1, dtype=np.int64)
    cur = np.zeros(n + 1, dtype=np.int64)

    for j_end in range(m + 1):
        for i_end in range(n + 1):
            new_score = -np.inf
            if i_end == 0 and j_end == 0:
                new_score = 0
            if i_end > 0:
                deletion_score = cur[i_end - 1] - 1
                if deletion_score > new_score:
                    new_score = deletion_score
            if j_end > 0:
                insertion_score = prev[i_end] - 1
                if insertion_score > new_score:
                    new_score = insertion_score
            if i_end > 0 and j_end > 0:
                match_score = prev[i_end - 1] + delta(v[i_end - 1], w[j_end - 1])
                if match_score > new_score:
                    new_score = match_score

            cur[i_end] = new_score

        prev = cur
        cur = np.zeros(n + 1, dtype=np.int64)

    return prev


def hirschberg(X: str, Y: str):
    Z = ''
    W = ''
    n = len(X)
    m = len(Y)
    if n == 0:
        Z = '-' * m
        W = Y
    elif m == 0:
        Z = X
        W = '-' * n
    elif n == 1:  # Needleman-Wunsch for single character case
        match_idx = Y.find(X)
        Z = (X + '-' * (m - 1)) if match_idx == -1 \
            else ('-' * match_idx + X + '-' * (m - match_idx - 1))
        W = Y
    elif m == 1:  # Needleman-Wunsch for single character case
        match_idx = X.find(Y)
        Z = X
        W = (Y + '-' * (n - 1)) if match_idx == -1 \
            else ('-' * match_idx + Y + '-' * (n - match_idx - 1))
    else:
        j = m // 2
        score_left = needleman_wunsch_score(X, Y[:j])
        score_right = needleman_wunsch_score(X[::-1], Y[-1:j - 1:-1])
        i = np.argmax(score_left + score_right[::-1])
        Z1, W1 = hirschberg(X[:i], Y[:j])
        Z2, W2 = hirschberg(X[i:], Y[j:])
        Z = Z1 + Z2
        W = W1 + W2

    return (Z, W)


def space_efficient_local_align(v: str, w: str):
    alignments = []
    score, windows = find_windows(v, w)
    for i_beg, j_beg, i_end, j_end in windows:
        alignments.append(hirschberg(v[i_beg:i_end], w[j_beg:j_end]))
    return score, alignments


def main():
    parser = argparse.ArgumentParser(description='Local alignment ...')
    parser.add_argument('query_seq', type=str, help='Query sequence for alignment')
    parser.add_argument('out_file', type=str, help='Output file for alignment results')
    parser.add_argument('-n', '--count', type=int, default=10, help='Number of top results to return (default 10)')
    args = parser.parse_args()

    query_seq: str = args.query_seq
    out_file: str = args.out_file
    top_n: int = args.count
    top_n = 5

    data_path = '../scrubbed-viral-data/scrubbed_sequences.csv'
    
    df = pd.read_csv(data_path)

    search_results = []
    peak_memory = 0
    process = psutil.Process(os.getpid())

    start_time = time.time()
    for _, row in tqdm(df.iterrows(), total=len(df)):
        score, alignments = space_efficient_local_align(query_seq, row['Sequence'])
        search_results.append({
            'score': score,
            'description': row['Description'],
            'alignments': alignments
        })
        # Check current memory usage
        mem_info = process.memory_info().rss  # in bytes
        if mem_info > peak_memory:
            peak_memory = mem_info

    search_results.sort(key=lambda x: x['score'], reverse=True)

    with open(out_file, 'w') as f:
        json.dump(search_results[:top_n], f, indent=4)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total runtime: {elapsed_time:.2f} seconds")
    print(f"Peak memory usage: {peak_memory/(1024*1024):.2f} MB")

if __name__ == '__main__':
    main()