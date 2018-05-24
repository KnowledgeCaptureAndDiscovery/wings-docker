import json
import urllib
from .auth import Auth


class ManageResource(Auth):
    def get_machine(self, resid):
        params = {'resid': resid}
        resp = self.session.get(self.server + '/common/resources/getMachineJSON?' +
                                urllib.urlencode(params))
        return resp.json()

    def save_machine(self, mid, machine_data):
        params = {'resid': mid, 'json': json.dumps(machine_data)}
        self.session.post(
            self.server + '/common/resources/saveMachineJSON', params)
