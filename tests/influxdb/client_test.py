# -*- coding: utf-8 -*-
import requests
import nose.tools
from mock import patch

from influxdb import InfluxDBClient


def _build_response_object(status_code=200, content=""):
    resp = requests.Response()
    resp.status_code = 200
    resp.content = content
    return resp


class TestInfluxDBClient(object):
    def test_switch_database(self):
        cli = InfluxDBClient('host', 8086, 'username', 'password', 'database')
        cli.switch_database('another_database')
        assert cli._database == 'another_database'

    def test_switch_username(self):
        cli = InfluxDBClient('host', 8086, 'username', 'password', 'database')
        cli.switch_username('another_username', 'another_password')
        assert cli._username == 'another_username'
        assert cli._password == 'another_password'
