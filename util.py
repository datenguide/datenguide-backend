from slugify import slugify_de


def slugify(value, to_lower=True, separator='-'):
    return slugify_de(value, to_lower=to_lower, separator=separator)


def get_fields_from_info(info):
    return {
        f.name.value: {
            a.name.value: a.value.value for a in f.arguments
        } for f in info.field_asts[0].selection_set.selections
    }


field_tmpl = """
**{name}**

*aus GENESIS-Statistik "{source[title_de]}" ({source[name]})*

{description}
"""


def get_field_description(info):
    return field_tmpl.format(**info).strip()


arg_tmpl = """
{name}

*Mögliche Werte:*

{values}
"""


def get_arg_description(info):
    return arg_tmpl.format(
        name=info['name'],
        values='\n\n'.join(['**{value}** - {name}'.format(**v) for v in info['values']])
    ).strip()
