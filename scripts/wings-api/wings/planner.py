import os
import re
import json
from .userop import UserOperation

class Planner(UserOperation):

	def __init__(self, server, userid, domain, template):
		super(Planner, self).__init__(server, userid, domain)
		self.libns = self.get_export_url() + "data/library.owl#";
		self.wflowns = self.get_export_url() + "workflows/" + template + ".owl#";
		self.wflowid = self.wflowns + template;

	def _get_input(self, val):
		if isinstance(val, basestring) and val.startswith('file:'):
			return self.libns + val[5:]
		else:
			return val

	def get_expansions(self, inputs):
		postdata = [('__template_id', self.wflowid), ('__cbindings', '{}'), ('__paramdtypes', '{}')]
		for invar in inputs:
			if type(inputs[invar]) is list:
				for val in inputs[invar]:
					postdata.append((invar, self._get_input(val)))
			else:
				postdata.append((invar, self._get_input(inputs[invar])))
		#print postdata
		resp = self.session.post( self.get_request_url() + 'plan/getExpansions', data=postdata )
		return resp.json()

	def select_template(self, templates):
		from sys import version_info
		py3 = version_info[0] > 2 

		i = 1
		num = len(templates)
		for tpl in templates:
			print "%s. %s" % (i, self.get_template_description(tpl['template']))
			i += 1
		index = 0
		while True: 
			if py3:
  				index = int(input("Please enter your selection: "))
			else:
  				index = int(raw_input("Please enter your selection: "))
			if index < 1 or index > num:
				print "Invalid Selection. Try again"
			else:
				break
		return templates[index-1]

	def get_template_description(self, template):
		regex = re.compile(r"^.*#")
		components = {}
		for node in template['Nodes']:
			comp = regex.sub("", node['componentVariable']['binding']['id'])
			if comp in components:
				components[comp] += 1
			else:
				components[comp] = 1

		description = regex.sub("", template['id']) + " ( "
		i = 0;
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
		resp = self.session.post( self.get_request_url() + 'executions/runWorkflow', data=postdata )
		regex = re.compile(r"^.*#")
		return regex.sub("", resp.text)
		
