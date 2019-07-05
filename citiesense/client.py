import tortilla


class APIKeyMissingError(Exception):
    pass


class Client(object):
    def __init__(self, key=None, host="https://api.citiesense.com", **kwargs):
        if key is None:
            raise APIKeyMissingError("All methods require an API key.")
        kwargs.update({ 'extension': 'json' })
        api = tortilla.wrap(host, **kwargs)
        api.config.headers["X-Api-Key"] = key
        self.api = api

    def community(self, id):
        return self.api.community(id)
