from .api import Api


class HighLevelSyncApi(Api):

    def __init__(self, root, tokens=None):
        super().__init__(root)
        self.tokens = tokens

    def join_barrier(self, parties, party, additional_tokens=None):
        sync_id = super().post_sync('control-flow', 'barrier', parameters={
            'tokens': HighLevelSyncApi.concat_nullable_arrays(self.tokens, additional_tokens)})
        states = {party: False for party in parties}
        super().put_sync(sync_id, states)
        while not all(states.values()):
            super().patch_sync(sync_id, {party: True})
            states = super().get_sync(sync_id)
        return None

    def clear_barrier(self, additional_tokens=None):
        sync_id = super().post_sync('control-flow', 'barrier', parameters={
            'tokens': HighLevelSyncApi.concat_nullable_arrays(self.tokens, additional_tokens)})
        super().delete_sync(sync_id)

    def send_broadcast(self, content, additional_tokens=None):
        sync_id = super().post_sync('control-flow', 'broadcast', parameters={
            'tokens': HighLevelSyncApi.concat_nullable_arrays(self.tokens, additional_tokens)})
        return super().put_sync(sync_id, content)

    def receive_broadcast(self, additional_tokens=None):
        sync_id = super().post_sync('control-flow', 'broadcast', parameters={
            'tokens': HighLevelSyncApi.concat_nullable_arrays(self.tokens, additional_tokens)})
        return super().get_sync(sync_id)

    def clear_broadcast(self, additional_tokens=None):
        sync_id = super().post_sync('control-flow', 'broadcast', parameters={
            'tokens': HighLevelSyncApi.concat_nullable_arrays(self.tokens, additional_tokens)})
        return super().delete_sync(sync_id)

    def wait_for_broadcast(self, additional_tokens=None):
        response = None
        while not response:
            response = self.receive_broadcast(additional_tokens)
        return response

    @staticmethod
    def concat_nullable_arrays(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return a + b
