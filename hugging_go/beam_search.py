from collections import namedtuple
from math import log
from heapq import nlargest
import time

Candidate = namedtuple('Candidate', ['sequence', 'next_color', 'label', 'scores', 'score'])

def beam_search(
    pipe,
    sequence,
    next_color,
    depth=6,
    k=3,
    time_limit=None,
    return_all_candidates=False
):
    start_time = time.monotonic()
    candidates = [
        Candidate(sequence=sequence, next_color=next_color, label=None, scores=[], score=0.0)
    ]

    while depth > 0 and (time_limit is None or (time.monotonic() - start_time) < time_limit):
        new_candidates = []

        for candidate in candidates:
            for step in pipe(candidate.sequence, candidate.next_color):
                new_candidates.append(
                    Candidate(
                        sequence=candidate.sequence + [step['label']],
                        next_color=candidate.next_color.opposite(),
                        label=candidate.label or step['label'],
                        scores=candidate.scores + [step['score']],
                        score=candidate.score + log(step['score'] + 1e-8)
                    )
                )

        depth -= 1
        candidates = nlargest(
            k,
            new_candidates,
            key=lambda c: c.score
        )

    if return_all_candidates:
        return candidates
    else:
        return max(candidates, key=lambda c: c.score)
