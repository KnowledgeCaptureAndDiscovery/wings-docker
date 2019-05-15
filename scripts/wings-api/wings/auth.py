import os
import sys
import requests
from pprint import pprint


class Auth(object):

    def __init__(self, server, internal_server, userid):
        self.session = requests.Session()
        self.server = server
        self.userid = userid
        self.internal_server = internal_server
        if internal_server is None:
            self.internal_server = server

    def login(self, password):
        response = self.session.get(self.server + '/sparql')
        data = {'j_username': self.userid, 'j_password': password}
        response = self.session.post(self.server + '/j_security_check', data)
        if response.status_code != 200 and response.status_code != 403:
            return False
        return True

    def logout(self):
        self.session.get(self.server + '/jsp/logout.jsp')
