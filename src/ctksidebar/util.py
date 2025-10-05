def resolve_padding(padding: int|tuple[int, int], index: int) -> int:
    if isinstance(padding, int):
        return padding
    elif isinstance(padding, tuple) and len(padding) == 2:  
        return padding[0 if index == 0 else 1]
    else:
        raise ValueError("Padding must be an int or a tuple of two ints")