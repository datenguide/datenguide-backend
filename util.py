from slugify import slugify_de


def slugify(value, to_lower=True, separator='-'):
    return slugify_de(value, to_lower=to_lower, separator=separator)


def get_fields_from_info(info):
    return {
        f.name.value: {
            a.name.value: a.value.value for a in f.arguments
        } for f in info.field_asts[0].selection_set.selections
    }
