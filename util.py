from slugify import slugify_de

# import settings


def slugify(value, to_lower=True, separator='-'):
    return slugify_de(value, to_lower=to_lower, separator=separator)


# def flatten_column_names(rows, start=settings.COLNAMES_START, end=settings.COLNAMES_END):
#     """
#     return column names from multi-row naming

#     rows: get from `open(csvfile).readlines()`
#     """
#     cells = [[cell.strip() for cell in row.split(';')] for row in rows[start:end]]
#     return ['_'.join([slugify(cells[j][i]) for j in range(len(cells))])
#             for i in range(len(cells[-1]))]
