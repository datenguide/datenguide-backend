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


def render(items, html):
    for key, info in items:
        html += '<section class="doc-item">'
        html += '<h1 class="doc-item__title">%s</h1>' % info['meta']['name']
        html += '<code class="doc-item__key">%s</code>' % key
        html += '<p class="doc-item__description">%s</p>' % info['meta']['description']
        # FIXME how to render nested keys
        # if info['children'].items():
        #     render(info['children'].items(), html)
        html += '</section>'
    return html


doc_content = render(make_doc_dict().items(), '')
