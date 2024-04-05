from .vertex import Vertex

from collections import namedtuple
import re

Sgf = namedtuple('Sgf', ['success', 'sequence', 'komi', 'winner'])

def _find_all_properties(name, text):
    pattern = f'[^A-Z]({name})((?:\\[[^\\]]*\\])+)'

    for match in re.finditer(pattern, text):
        for value in re.findall(r'\[([^\]]*)\]', match[2]):
            yield (match[1], value)

def _find_single_property(name, text, map_fn):
    properties = list(_find_all_properties(name, text))

    if properties:
        (_, value) = properties[0]

        return map_fn(value) if value else None

def _sgf_to_gtp(text, allow_pass=False):
    vertex = Vertex.from_sgf(text)

    if not vertex.is_valid():
        if allow_pass:
            return 'pass'
        raise ValueError(f'unrecognized coordinate: {text}')
    return vertex.as_gtp()

def parse_sgf(sgf):
    try:
        return Sgf(
            success=True,
            sequence=[
                property[-1] + _sgf_to_gtp(vertex, allow_pass=property in ['B', 'W'])
                for (property, vertex) in _find_all_properties('AB|AW|B|W', sgf)
            ],
            komi=_find_single_property('KM', sgf, lambda x: float(x)),
            winner=_find_single_property('RE', sgf, lambda x: x[0])
        )
    except ValueError:
        return Sgf(
            success=False,
            sequence=[],
            komi=0.5,
            winner='?'
        )
