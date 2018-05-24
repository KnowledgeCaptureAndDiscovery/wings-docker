import os
import re
import json
from .userop import UserOperation


class Planner(UserOperation):

    def __init__(self, server, userid, domain, template):
        super(Planner, self).__init__(server, userid, domain)
        self.libns = self.get_export_url() + "data/library.owl#"
        self.wflowns = self.get_export_url() + "workflows/" + template + ".owl#"
        self.wflowid = self.wflowns + template
        self.xsdns = "http://www.w3.org/2001/XMLSchema#"

    def _set_bindings(self, invar, val, dataBindings, parameterBindings, parameterTypes):
        if isinstance(val, basestring) and val.startswith('file:'):
            data = dataBindings.get(self.wflowns + invar, [])
            data.append(self.libns + val[5:])
            dataBindings[self.wflowns + invar] = data
        else:
            parameterBindings[self.wflowns + invar] = val
            typeid = self.xsdns + "string"
            if type(val) is int:
                typeid = self.xsdns + "integer"
            elif type(val) is float:
                typeid = self.xsdns + "float"
            elif type(val) is bool:
                typeid = self.xsdns + "boolean"
            parameterTypes[self.wflowns + invar] = typeid

    def get_expansions(self, inputs):
        postdata = [('templateId', self.wflowid),
                    ('componentBindings', '{}'), ('parameterBindings', '{}')]
        dataBindings = dict()
        parameterBindings = dict()
        parameterTypes = dict()
        for invar in inputs:
            if type(inputs[invar]) is list:
                for val in inputs[invar]:
                    self._set_bindings(
                        invar, val, dataBindings, parameterBindings, parameterTypes)
            else:
                self._set_bindings(
                    invar, inputs[invar], dataBindings, parameterBindings, parameterTypes)
        postdata = {
            "templateId": self.wflowid,
            "dataBindings": dataBindings,
            "parameterBindings": parameterBindings,
            "parameterTypes": parameterTypes,
            "componentBindings": dict()
        }
        resp = self.session.post(
            self.get_request_url() + 'plan/getExpansions', json=postdata)
        return resp.json()

    def select_template(self, templates):
        from sys import version_info
        py3 = version_info[0] > 2

        i = 1
        num = len(templates)
        for tpl in templates:
            print("%s. %s" %
                  (i, self.get_template_description(tpl['template'])))
            i += 1
        index = 0
        while True:
            if py3:
                index = int(input("Please enter your selection: "))
            else:
                index = int(raw_input("Please enter your selection: "))
            if index < 1 or index > num:
                print("Invalid Selection. Try again")
            else:
                break
        return templates[index - 1]

    def get_template_description(self, template):
        regex = re.compile(r"^.*#")
        components = {}
        for nodeid in template['Nodes']:
            node = template['Nodes'][nodeid]
            comp = regex.sub("", node['componentVariable']['binding']['id'])
            if comp in components:
                components[comp] += 1
            else:
                components[comp] = 1

        description = regex.sub("", template['id']) + " ( "
        i = 0
        for comp in components:
            if i > 0:
                description += ", "
            description += str(components[comp]) + " " + comp
            i += 1
        description += " )"
        return description

    def run_workflow(self, template, seed):
        postdata = {
            'template_id': seed["template"]["id"],
            'json': json.dumps(template["template"]),
            'constraints_json': json.dumps(template["constraints"]),
            'seed_json': json.dumps(seed["template"]),
            'seed_constraints_json': json.dumps(seed["constraints"])
        }
        resp = self.session.post(self.get_request_url(
        ) + 'executions/runWorkflow', data=postdata)
        regex = re.compile(r"^.*#")
        return regex.sub("", resp.text)
