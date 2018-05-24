import json
import argparse
import wings.resource

localhost = 'http://www.wings-workflows.org/ontology/resource.owl#Localhost'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument("-u", "--userid", help="Portal userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal password", default="4dm1n!23")
parser.add_argument("-m", "--machine", help="Machine id", default=localhost)
parser.add_argument("-gm", "--get_machine",
                    help="Get Machine details", action="store_true")
parser.add_argument("-sm", "--save_machine",
                    help="Save Machine details", action="store_true")
parser.add_argument("-f", "--machine_file",
                    help="File to get Machine details from")
args = parser.parse_args()

# Create manage domain api
res = wings.ManageResource(args.server, args.userid)

# Login with password
if res.login(args.password):
    if args.machine:
        m = res.get_machine(args.machine)
        if args.get_machine:
            print m
        elif args.save_machine:
            f = args.machine_file
            if f != None:
                with open(f) as fd:
                    fjson = json.load(fd)
                    swids = m["softwareIds"]
                    for swid in fjson["softwares"]:
                        if swid not in m["softwareIds"]:
                            m["softwareIds"].append(swid)
                    for fkey, fvalue in fjson["environment"].items():
                        existing = False
                        for menv in m["environmentValues"]:
                            if fkey == menv['variable']:
                                menv['value'] = fvalue
                                existing = True
                        if not existing:
                            m["environmentValues"].append({
                                'variable': fkey, 'value': fvalue})
                    res.save_machine(args.machine, m)
    # Logout
    res.logout()
