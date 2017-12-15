from graphene import relay


class Node(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return '{}:{}'.format(type, id)

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        type, id = global_id.split(':')
        if only_type:
            # We assure that the node type that we want to retrieve
            # is the same that was indicated in the field type
            assert type == only_type._meta.name, 'Received not compatible node.'

        # FIXME reorganize code to avoid circular imports
        from stores import STORES
        return STORES[type].get(id)
