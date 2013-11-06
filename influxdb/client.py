# -*- coding: utf-8 -*-
"""
python client for influxdb
"""
import requests
import json


class InfluxDBClient(object):
    """
    InfluxDB Client
    """
    def __init__(self, host, port, username, password, database):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._baseurl = "http://{0}:{1}".format(self._host, self._port)

        self._headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'}

    # Change member variables

    def switch_database(self, database):
        """
        Change client database

        Parameters
        ----------
        database : string
        """
        self._database = database

    def switch_username(self, username, password):
        """
        Change client username

        Parameters
        ----------
        username : string
        password : string
        """
        self._username = username
        self._password = password

    ###
    # Administration & Security

    ###
    # Creating and Dropping Databases

    def create_database(self, database):
        """
        Create a database

        Parameters
        ----------
        database: string
            database name
        """
        response = requests.post("{0}/db?u={1}&p={2}".format(
            self._baseurl,
            self._username,
            self._password),
            data=json.dumps({'name': database}),
            headers=self._headers)

        if response.status_code == 201:
            return True
        else:
            raise Exception(response.content)

    def delete_database(self, database):
        """
        Drop a database

        Parameters
        ----------
        database: string
            database name
        """
        response = requests.delete("{0}/db/{1}?u={2}&p={3}".format(
            self._baseurl,
            database,
            self._username,
            self._password))

        if response.status_code == 204:
            return True
        else:
            raise Exception(response.content)

    ###
    # Security

    ###
    # Limiting User Access

    def get_database_users(self):
        """
        Get list of database users
        """
        response = requests.get(
            "{0}/db/{1}/users?u={2}&p={3}".format(
                self._baseurl,
                self._database,
                self._username,
                self._password))

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def add_database_user(self, new_username, new_password):
        """
        Add database user
        """
        response = requests.post(
            "{0}/db/{1}/users?u={2}&p={3}".format(
                self._baseurl,
                self._database,
                self._username,
                self._password),
            data=json.dumps({
                'username': new_username,
                'password': new_password}),
            headers=self._headers)

        if response.status_code == 200:
            return True
        else:
            raise Exception(response.content)

    def update_database_password(self, username, new_password):
        """
        Update password
        """
        response = requests.post(
            "{0}/db/{1}/users/{2}?u={3}&p={4}".format(
                self._baseurl,
                self._database,
                username,
                self._username,
                self._password),
            data=json.dumps({
                'password': new_password}),
            headers=self._headers)

        if response.status_code == 200:
            if username == self._username:
                self._password = new_password
            return True
        else:
            raise Exception(response.content)

    def delete_database_user(self, username):
        """
        Delete database user
        """
        response = requests.delete(
            "{0}/db/{1}/users/{2}?u={3}&p={4}".format(
                self._baseurl,
                self._database,
                username,
                self._username,
                self._password))

        if response.status_code == 200:
            return True
        else:
            raise Exception(response.content)

    ###
    # Writing Data

    def write_points(self, data):
        """
        Write to multiple time series names
        """
        response = requests.post(
            "{0}/db/{1}/series?u={2}&p={3}".format(
                self._baseurl,
                self._database,
                self._username,
                self._password),
            data=json.dumps(data),
            headers=self._headers)

        if response.status_code == 200:
            return True
        else:
            raise Exception(response.content)

    def write_points_with_time_precision(self, data, time_precision='s'):
        """
        Write to multiple time series names
        """
        if time_precision not in ['s', 'm', 'u']:
            raise Exception("Invalid time precision is given.")

        response = requests.post(
            "{0}/db/{1}/series?u={2}&p={3}&time_precision={4}".format(
                self._baseurl,
                self._database,
                self._username,
                self._password,
                time_precision),
            data=json.dumps(data),
            headers=self._headers)

        if response.status_code == 200:
            return True
        else:
            raise Exception(response.content)

    def delete_points(self, name,
                      regex=None, start_epoch=None, end_epoch=None):
        pass

    ###
    # Regularly Scheduled Deletes

    ###
    # Querying Data
