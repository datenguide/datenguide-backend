from database import KEYS, get_key_info


def to_dict(t):
    return {k: to_dict(t[k]) for k in t}


def make_doc_dict(source=to_dict(KEYS), target={}):
    target['children'] = {}
    target = target['children']
    for key, value in source.items():
        target[key] = {}
        target[key]['meta'] = get_key_info(key)
        target[key]['children'] = make_doc_dict(value, target[key])
    return target


def render_key(key):
    return """
        <section class="doc-item">
        <h1 class="doc-item__title">{name}</h1>
        <code class="doc-item__key">{code}</code>
        <p class="doc-item__description">{description}</p>
        {children}
        </section>
    """.format(**key['meta'],
               children=''.join([render_key(k) for code, k in key['children'].items()
                                 if 'year' not in code]))


doc_content = ''.join([render_key(k) for k in make_doc_dict().values()])
