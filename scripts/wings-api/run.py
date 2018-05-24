import re
import json
import argparse
import wings.planner

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument(
    "-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal admin password", default="4dm1n!23")
parser.add_argument("-dom", "--domain", help="Portal domain")
parser.add_argument("-t", "--template", help="Template name")
parser.add_argument(
    "-a", "--auto", help="Automatically run first plan (non-interactive)", action="store_true")
parser.add_argument("-i", "--inputs", help="Inputs json file")
args = parser.parse_args()

# Create manage user api
planner = wings.Planner(args.server, args.userid, args.domain, args.template)

# Login with password
if planner.login(args.password):
    if args.inputs:
        with open(args.inputs) as ifile:
            inputs = json.load(ifile)
            ret = planner.get_expansions(inputs)
            if ret and ret['success']:
                seed = ret['data']['seed']
                templates = ret['data']['templates']
                template = templates[0]
                if not args.auto:
                    template = planner.select_template(templates)
                runid = planner.run_workflow(template, seed)
                print(runid)
    # Logout
    planner.logout()
