import os
import json
import argparse
import wings.component

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument(
    "-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal admin password", default="4dm1n!23")
parser.add_argument("-dom", "--domain", help="Portal domain")
parser.add_argument("-n", "--new", help="Create operation",
                    action="store_true")
parser.add_argument(
    "-x", "--delete", help="Delete operation", action="store_true")
parser.add_argument("-ct", "--component_type", help="Component type")
parser.add_argument("-pt", "--parent_type",
                    help="Component type's Parent (for creating new component type)")
parser.add_argument("-c", "--component_id", help="Component id")
parser.add_argument("-j", "--save_json",
                    help="Save json for component/type (filename with json for component/type)")
parser.add_argument("-l", "--component_location", help="Set component location")
parser.add_argument("-up", "--upload_component",
                    help="Upload component zip")
parser.add_argument(
    "-g", "--get", help="Get information (use either with component_id, component_type or none)", action="store_true")
args = parser.parse_args()

# Create manage user api
component = wings.ManageComponent(args.server, args.userid, args.domain)

# Login with password
if component.login(args.password):
    if args.new:
        if args.component_id:
            component.new_component(args.component_id, args.component_type)
        elif args.component_type:
            component.new_component_type(args.component_type, args.parent_type)
    elif args.delete:
        if args.component_id:
            component.del_component(args.component_id)
        elif args.component_type:
            component.del_component_type(args.component_type)
    elif args.get:
        if args.component_id:
            print(component.get_component_description(args.component_id))
        elif args.component_type:
            print(component.get_component_type_description(args.component_type))
        else:
            print(component.get_all_items())
    elif args.upload_component and args.component_id:
        print(component.upload_component(args.upload_component, args.component_id))
    elif args.save_json:
        with open(args.save_json) as cfile:
            jsonobj = json.load(cfile)
            if args.component_id:
                component.save_component(args.component_id, jsonobj)
            elif args.component_type:
                component.save_component_type(args.component_type, jsonobj)
    elif args.component_location and args.component_id:
        component.set_component_location(args.component_id, args.component_location)

    # Logout
    component.logout()
