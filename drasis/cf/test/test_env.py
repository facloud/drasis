from unittest import TestCase

from drasis.cf.env import Env


class TestEnv(TestCase):
    def setUp(self):
        self.env = Env({
            'PORT': 1234,
            'VCAP_SERVICES': """{
    "p-rabbitmq": [
        {
            "credentials": {
                "uri": "amqp://boo:baa@node123.rabbit-cloud.com:4532"
            }
        }
    ]
}""",
        })

    def test_it_extracts_port(self):
        self.assertEqual(self.env.get_port(), 1234)

    def test_when_port_not_defined(self):
        env = Env({})
        with self.assertRaises(Env.KeyNotFoundError):
            env.get_port()

    def test_when_port_is_invalid(self):
        env = Env({
            'PORT': 'abc'
        })
        with self.assertRaises(Env.InvalidValueError):
            env.get_port()

    def test_it_extracts_service_credentials(self):
        self.assertEqual(
            self.env.get_rabbitmq_uri('p-rabbitmq'),
            'amqp://boo:baa@node123.rabbit-cloud.com:4532'
        )

    def test_when_vcapservices_is_not_defined(self):
        env = Env({})
        with self.assertRaises(Env.KeyNotFoundError):
            env.get_rabbitmq_uri('p-rabbitmq')

    def test_when_vcapservices_is_invalid_json(self):
        env = Env({
            'VCAP_SERVICES': '{]{'
        })
        with self.assertRaises(Env.InvalidValueError):
            env.get_rabbitmq_uri('p-rabbitmq')

    def test_when_vcapservices_doesnot_contain_service(self):
        env = Env({
            'VCAP_SERVICES': '{}'
        })
        with self.assertRaises(Env.ServiceNotFoundError):
            env.get_rabbitmq_uri('p-rabbitmq')

    def test_when_vcapservices_contains_service_but_invalid(self):
        env = Env({
            'VCAP_SERVICES': '{"p-rabbitmq": {}}'
        })
        with self.assertRaises(Env.InvalidValueError):
            env.get_rabbitmq_uri('p-rabbitmq')

    def test_when_vcapservices_contains_service_but_empty(self):
        env = Env({
            'VCAP_SERVICES': '{"p-rabbitmq": []}'
        })
        with self.assertRaises(Env.ServiceNotFoundError):
            env.get_rabbitmq_uri('p-rabbitmq')

    def test_when_vcapservices_isnot_formed_as_expected(self):
        env = Env({
            'VCAP_SERVICES': '{"p-rabbitmq": [{"credentials": {}}]}'
        })
        with self.assertRaises(Env.InvalidValueError):
            env.get_rabbitmq_uri('p-rabbitmq')
