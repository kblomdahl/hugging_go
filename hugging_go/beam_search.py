from collections import namedtuple
from math import log
from heapq import nlargest

Candidate = namedtuple('Candidate', ['sequence', 'label', 'score'])

def beam_search(
    pipe,
    sequence,
    depth=6,
    k=3
):
    candidates = [
        Candidate(sequence=sequence, label=None, score=0.0)
    ]

    while depth > 0:
        new_candidates = []

        for candidate in candidates:
            for step in pipe(candidate.sequence):
                new_candidates.append(
                    Candidate(
                        sequence=candidate.sequence + [step['label']],
                        label=candidate.label or step['label'],
                        score=candidate.score + log(step['score'])
                    )
                )

        depth -= 1
        candidates = nlargest(
            k,
            new_candidates,
            key=lambda c: c.score
        )

    return max(candidates, key=lambda c: c.score)
