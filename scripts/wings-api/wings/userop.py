from .auth import Auth


class UserOperation(Auth):

    def __init__(self, server, internal_server, userid, domain):
        super(UserOperation, self).__init__(server, internal_server, userid)
        self.domain = domain

    def get_request_url(self):
        return self.server + "/users/" + self.userid + "/" + self.domain + "/"

    def get_export_url(self):
        return self.internal_server + "/export/users/" + self.userid + "/" + self.domain + "/"
