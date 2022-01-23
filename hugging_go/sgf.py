from .vertex import Vertex

import re

def parse_sgf_sequence(sgf):
    try:
        return [
            vertex.as_gtp() if vertex.is_valid() else 'pass'
            for vertex in [
                Vertex.from_sgf(vertex)
                for vertex in re.findall(r'[BW]\[([a-z]{0,2})\]', sgf)
            ]
        ]
    except ValueError:
        return []
