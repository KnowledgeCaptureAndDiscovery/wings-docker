import os
import re
import json
from .userop import UserOperation


class ManageRun(UserOperation):

    def __init__(self, server, internal_server, userid, domain):
        super(ManageRun, self).__init__(server, internal_server, userid, domain)

    def get_run_id(self, runid):
        if not re.match(r"(http:|https:)//", runid):
            return self.get_export_url() + "executions/" + runid + ".owl#" + runid;
        else:
            return runid

    def get_all_runs(self):
        resp = self.session.get(
            self.get_request_url() + 'executions/getRunList')
        return resp.json()

    def get_run_details(self, runid):
        runid = self.get_run_id(runid)
        postdata = {'run_id': runid}
        resp = self.session.post(
            self.get_request_url() + 'executions/getRunDetails', postdata)
        return resp.json()

