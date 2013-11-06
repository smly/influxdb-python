# -*- coding: utf-8 -*-
import requests
from nose.tools import raises
from mock import patch

from influxdb import InfluxDBClient


def _build_response_object(status_code=200, content=""):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = content
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

    def test_create_database(self):
        with patch.object(requests, 'post') as mocked_post:
            mocked_post.return_value = _build_response_object()
            cli = InfluxDBClient('host', 8086, 'username', 'password', 'db')
            assert cli.create_database('new_db') is True

    @raises(Exception)
    def test_creata_database_fails(self):
        with patch.object(requests, 'post') as mocked_post:
            mocked_post.return_value = _build_response_object(status_code=401)
            cli = InfluxDBClient('host', 8086, 'username', 'password', 'db')
            cli.create_database('new_db')

    def test_delete_database(self):
        with patch.object(requests, 'delete') as mocked_post:
            mocked_post.return_value = _build_response_object()
            cli = InfluxDBClient('host', 8086, 'username', 'password', 'db')
            assert cli.delete_database('old_db') is True

    @raises(Exception)
    def test_delete_database_fails(self):
        with patch.object(requests, 'delete') as mocked_post:
            mocked_post.return_value = _build_response_object(status_code=401)
            cli = InfluxDBClient('host', 8086, 'username', 'password', 'db')
            cli.delete_database('old_db')


