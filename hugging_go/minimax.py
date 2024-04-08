""" Minimax algorithm with tail-free sampling and α-β pruning.

An implementation of minimax with a few tweaks to make it more sample efficient:
  - tail-free sampling (tfs) to reduce the number of nodes visited.
  - α-β pruning to reduce the number of nodes visited.
    - ordering of the nodes by score to increase the likelihood of pruning.
"""

import time
import numpy as np
from collections import namedtuple

Candidate = namedtuple('Candidate', ['label', 'score', 'value', 'child'])

def tail_free_sampling(candidates, z=0.95):
    candidates = sorted(candidates, key=lambda cand: cand['score'], reverse=True)
    scores = np.array([cand['score'] for cand in candidates])
    delta_2 = np.abs(np.diff(scores, n=2, prepend=[0, 0]))
    normalized_delta_2 = delta_2 / np.sum(delta_2)
    cumsum_delta_2 = np.cumsum(normalized_delta_2)

    return [
        candidates[i]
        for i in range(len(candidates))
        if cumsum_delta_2[i] <= z
    ]

def _minimax(
    pipe,
    sequence,
    next_player,
    alpha,
    beta,
    depth,
    tfs_z=0.95,
    return_all_candidates=False,
    past_key_values=None
):
    [candidates, value, next_past_key_values] = pipe(sequence, next_player, past_key_values=past_key_values)
    if depth <= 0:
        return Candidate(label=None, score=None, value=value, child=None)

    all_candidates = []
    for candidate in tail_free_sampling(candidates, z=tfs_z):
        new_candidate = _minimax(
            pipe=pipe,
            sequence=sequence + [candidate['label']],
            next_player=next_player.opposite(),
            alpha=-beta,
            beta=-alpha,
            depth=depth - 1,
            tfs_z=tfs_z,
            return_all_candidates=False,
            past_key_values=next_past_key_values
        )

        if new_candidate:
            if new_candidate.value > beta:
                break
            if new_candidate.value > alpha:
                alpha = new_candidate.value

            all_candidates.append(Candidate(
                label=candidate['label'],
                score=candidate['score'],
                value=-new_candidate.value,
                child=new_candidate
            ))

    if return_all_candidates:
        return all_candidates
    elif all_candidates == []:
        return None
    else:
        return min(all_candidates, key=lambda cand: cand.value)

def minimax(
    pipe,
    sequence,
    next_player,
    depth=2,
    tfs_z=0.95,
    time_limit=None,
    return_all_candidates=False
):
    if time_limit is None:
        return [_minimax(pipe, sequence, next_player, -1.0, 1.0, depth, tfs_z, return_all_candidates), depth]
    else:
        start_time = time.monotonic()
        current_depth = 1
        so_far = None

        while so_far is None or (current_depth <= depth and (time.monotonic() - start_time) < time_limit):
            so_far = _minimax(pipe, sequence, next_player, -1.0, 1.0, current_depth, tfs_z, return_all_candidates)
            current_depth += 1

        return [so_far, current_depth - 1]
