import json
from json.decoder import JSONDecodeError


class Env(object):
    class Error(Exception):
        pass

    class KeyNotFoundError(Error):
        pass

    class InvalidValueError(Error):
        pass

    class ServiceNotFoundError(Error):
        pass

    def __init__(self, env):
        self.env_dict = env

    def get_port(self):
        if 'PORT' not in self.env_dict:
            raise Env.KeyNotFoundError(
                '`PORT` not defined in the environment variables'
            )

        try:
            return int(self.env_dict['PORT'])
        except ValueError as ex:
            raise Env.InvalidValueError(ex)

    def get_rabbitmq_uri(self, service_name):
        if 'VCAP_SERVICES' not in self.env_dict:
            raise Env.KeyNotFoundError(
                '`VCAP_SERVICES` not defined in the environment variables'
            )

        try:
            services = json.loads(self.env_dict['VCAP_SERVICES'])
        except JSONDecodeError as ex:
            raise Env.InvalidValueError(ex)

        if service_name not in services:
            raise Env.ServiceNotFoundError(
                '`{:s}` service was not found in `VCAP_SERVICES`'.format(
                    service_name
                )
        )
        service_instances = services[service_name]

        if type(service_instances) is not list:
            raise Env.InvalidValueError(
                '`{:s}` was found in `VCAP_SERVICES`, '.format(service_name) + \
                'but it\'s not a list'
            )

        if len(service_instances) == 0:
            raise Env.ServiceNotFoundError(
                '`{:s}` was found in `VCAP_SERVICES`, '.format(service_name) + \
                'but it\'s empty'
            )

        try:
            return services['p-rabbitmq'][0]['credentials']['uri']
        except TypeError as ex:
            raise Env.InvalidValueError(ex)
        except KeyError as ex:
            raise Env.InvalidValueError(ex)
