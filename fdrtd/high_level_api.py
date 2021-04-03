from .api import Api
from .high_level_sync_api import HighLevelSyncApi


class HighLevelApi(Api):

    def __init__(self, network_definition, tokens=None):
        self.network_nodes = network_definition['nodes']
        self.network_myself = network_definition['myself']
        super().__init__(self.network_nodes[self.network_myself])
        self.sync_api = HighLevelSyncApi(network_definition['sync'], tokens)
        self.network_id = super().create_network(network_definition)

    def compute(self, protocol, microservice, data, parameters=None, tokens=None):
        data_id = super().upload_data(data)
        task_id = self.join_task(protocol, microservice, tokens)
        super().input_data(task_id, data_id, parameters)
        self.sync_api.join_barrier(range(len(self.network_nodes)), self.network_myself, tokens)
        result = self.wait_for_result(task_id)
        if self.network_myself == 0:
            self.sync_api.clear_barrier(tokens)
            self.sync_api.clear_broadcast(tokens)
        return result

    def join_task(self, protocol, microservice, tokens):
        if self.network_myself == 0:
            task_id = super().create_task(protocol, microservice, self.network_id)
            invitation = super().create_invitation(task_id)
            self.sync_api.send_broadcast(invitation, tokens)
            return task_id
        else:
            invitation = self.sync_api.wait_for_broadcast(tokens)
            task_id = super().accept_invitation(protocol, microservice, self.network_id, invitation)
            return task_id

    def wait_for_result(self, task_id):
        response = None
        while response is None:
            response = super().get_result(task_id)
        return response
