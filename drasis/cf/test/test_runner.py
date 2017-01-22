import os
import logging
from urllib import request

from unittest2 import TestCase

from nameko.rpc import rpc
from nameko.standalone.rpc import ClusterRpcProxy

from drasis.test.logger import configure_global_logger
from drasis.cf.runner import Config, Runner


class TestService(object):
    name = 'test_service'

    @rpc
    def echo(self, msg):
        return msg + ' back'


class TestRunner(TestCase):
    def setUp(self):
        # setup global logger
        configure_global_logger()

        # AMQP URI
        rabbitmq_port = int(os.environ.get('TEST_DRASIS_RABBITMQ_PORT', 15672))
        self.amqp_uri = 'amqp://guest:guest@localhost:{:d}'.format(
            rabbitmq_port
        )
        logging.debug('amqp_uri = {:s}'.format(self.amqp_uri))

        # setup runner
        self.runner = Runner(Config(self.amqp_uri, '0.0.0.0:12222'))

        # start
        self.runner.add_service(TestService)
        self.runner.start()

    def tearDown(self):
        self.runner.stop()

    def test_health_endpint(self):
        self.assertEqual(
            request.urlopen("http://127.0.0.1:12222/health").read(),
            b'OK'
        )

    def test_rpc(self):
        config = {'AMQP_URI': self.amqp_uri}
        with ClusterRpcProxy(config) as proxy:
            self.assertEqual(
                proxy.test_service.echo('hello'),
                'hello back'
            )
