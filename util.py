from slugify import slugify_de


def slugify(value, to_lower=True, separator='-'):
    return slugify_de(value, to_lower=to_lower, separator=separator)
