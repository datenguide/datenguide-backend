from graphene import relay

from database import DB


class Node(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return '{}:{}'.format(type, id)

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        type = global_id.split(':')[0]
        if only_type:
            # We assure that the node type that we want to retrieve
            # is the same that was indicated in the field type
            assert type == only_type._meta.name, 'Received not compatible node.'

        node = DB
        for attr in global_id.split(':')[1:]:
            node = node[attr]
        from models import Data  # FIXME reorganize code to avoid circular imports
        return Data(id=node.id, data=[Data(**d) for d in node.data])
