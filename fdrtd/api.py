from .low_level_api import LowLevelApi


class Api(LowLevelApi):

    def __init__(self, root):
        super().__init__(root)

    def get_capabilities(self):
        return super().get('/capabilities')

    def create_network(self, network):
        return super().post('/networks', body=network)

    def set_network(self, network_id, network):
        return super().put('/networks', network_id, body=network)

    def get_network(self, network_id):
        return super().get('/networks', network_id)

    def delete_network(self, network_id):
        return super().delete('/networks', network_id)

    def upload_data(self, data=None, data_format='raw'):
        return super().post('/data', 'upload', data_format, body={'data': data})

    def create_data(self, family, microservice, parameters):
        return super().post('/data', family, microservice, body=parameters)

    def delete_data(self, data_id):
        return super().delete('/data', data_id)

    def create_script(self, family, microservice, parameters=None):
        return super().post('/scripts', family, microservice, body=parameters)

    def execute_script(self, script_id, parameters=None):
        return super().patch('/scripts', script_id, body=parameters)

    def delete_script(self, script_id):
        return super().delete('/scripts', script_id)

    def create_task(self, family, microservice, network_id, parameters=None):
        return super().post('/tasks', family, microservice, network_id, body=parameters)

    def accept_invitation(self, family, microservice, network_id, invitation):
        return super().patch('/tasks', family, microservice, network_id, body=invitation)

    def create_invitation(self, task_id):
        return super().get('/tasks', task_id)

    def delete_task(self, task_id):
        return super().delete('/tasks', task_id)

    def input_data(self, task_id, data_id, parameters=None):
        return super().put('/tasks', task_id, '/input', data_id, body=parameters)

    def get_result(self, task_id):
        return super().get('/tasks', task_id, '/result')

    def put_keylut(self, task_id, keylut):
        return super().put('/tasks', task_id, '/keylut', body=keylut)

    def patch_keylut(self, task_id, keylut):
        return super().patch('/tasks', task_id, '/keylut', body=keylut)

    def get_keylut(self, task_id):
        return super().get('/tasks', task_id, '/keylut')

    def delete_keylut(self, task_id):
        return super().delete('/tasks', task_id, '/keylut')

    def post_peertopeer(self, task_id, body=None):
        return super().post('/tasks', task_id, '/peertopeer', body=body)

    def put_peertopeer(self, task_id, body=None):
        return super().put('/tasks', task_id, '/peertopeer', body=body)

    def patch_peertopeer(self, task_id, body=None):
        return super().patch('/tasks', task_id, '/peertopeer', body=body)

    def get_peertopeer(self, task_id):
        return super().get('/tasks', task_id, '/peertopeer')

    def delete_peertopeer(self, task_id):
        return super().delete('/tasks', task_id, '/peertopeer')

    def post_sync(self, family, microservice, parameters=None):
        return super().post('/sync', family, microservice, body=parameters)

    def put_sync(self, sync_id, body):
        return super().put('/sync', sync_id, body=body)

    def patch_sync(self, sync_id, body):
        return super().patch('/sync', sync_id, body=body)

    def get_sync(self, sync_id):
        return super().get('/sync', sync_id)

    def delete_sync(self, sync_id):
        return super().delete('/sync', sync_id)
