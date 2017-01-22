"""
`drasis.cf.runner` is a module that provides the `NamekoRunner` class which
wraps the standard `nameko` runner to take care of running a single `nameko`
service while providing a health HTTP endpoint.
"""

import os
import json

import eventlet
eventlet.monkey_patch()  # noqa (code before rest of imports)

from nameko.web.handlers import http
from nameko.runners import ServiceRunner


class Config(object):
    def __init__(self, amqp_uri, health_endpoint='127.0.0.1:8080'):
        self.amqp_uri = amqp_uri
        self.health_endpoint = health_endpoint


class HealthService(object):
    name = 'health_service'

    @http('GET', '/')
    def get_method(self, req):
        return json.dumps(os.environ.__dict__)


class Runner(ServiceRunner):
    def __init__(self, config):
        ServiceRunner.__init__(self, {
            'AMQP_URI':             config.amqp_uri,
            'WEB_SERVER_ADDRESS':   config.health_endpoint
        })
        self.add_service(HealthService)
