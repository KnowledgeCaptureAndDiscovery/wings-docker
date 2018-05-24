import os
from .auth import Auth


class ManageDomain(Auth):

    def import_domain(self, url):
        data = {'domain': os.path.basename(url), 'location': url}
        self.session.post(self.server + '/users/' +
                          self.userid + '/domains/importDomain', data)

    def get_domain_details(self, domain):
        response = self.session.get(
            self.server + '/users/' + self.userid + '/domains/getDomainDetails?domain=' + domain)
        if response.text:
            return response.json()
        else:
            return None

    def select_default_domain(self, domain):
        data = {'domain': domain}
        self.session.post(self.server + '/users/' +
                          self.userid + '/domains/selectDomain', data)

    def delete_domain(self, domain):
        data = {'domain': domain}
        self.session.post(self.server + '/users/' +
                          self.userid + '/domains/deleteDomain', data)
