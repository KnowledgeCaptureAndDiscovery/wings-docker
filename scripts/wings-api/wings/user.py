import os
import json
from .auth import Auth


class ManageUser(Auth):

    def add_user(self, userid):
        data = {'userid': userid}
        response = self.session.post(
            self.server + '/users/common/list/addUser', data)
        if response.text == "OK":
            return True
        return False

    def get_user_details(self, userid):
        response = self.session.get(
            self.server + '/users/common/list/getUserJSON?userid=' + userid)
        if response.text:
            return response.json()
        else:
            return None

    def set_user_details(self, userid, password, fullname, isadmin):
        data = {'id': userid, 'fullname': fullname,
                'password': password, 'isAdmin': isadmin}
        postdata = {'userid': userid, 'json': json.dumps(data)}
        self.session.post(
            self.server + '/users/common/list/saveUserJSON', postdata)

    def delete_user(self, userid):
        data = {'userid': userid}
        self.session.post(self.server + '/users/common/list/removeUser', data)
