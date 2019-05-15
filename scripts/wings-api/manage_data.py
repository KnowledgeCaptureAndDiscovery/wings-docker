import os
import json
import argparse
import wings.data

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument("-is", "--internal_server", help="Wings internal server",
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
parser.add_argument("-dt", "--data_type", help="Data type")
parser.add_argument("-pt", "--parent_type",
                    help="Data type's Parent (for creating new data type)")
parser.add_argument("-d", "--data_id", help="Data id")
parser.add_argument("-m", "--save_metadata",
                    help="Save metadata for data (filename with json metadata)")
parser.add_argument("-pr", "--add_properties",
                    help="Add properties for data type (filename with json properties)")
parser.add_argument("-l", "--data_location", help="Set data location")
parser.add_argument("-up", "--upload_data",
                    help="Upload data from file for a data type")
parser.add_argument(
    "-g", "--get", help="Get information (use either with data_id, data_type or none)", action="store_true")
args = parser.parse_args()

# Create manage user api
data = wings.ManageData(args.server, args.internal_server, args.userid, args.domain)

# Login with password
if data.login(args.password):
    if args.new:
        if args.data_id:
            data.add_data_for_type(args.data_id, args.data_type)
        elif args.data_type:
            data.new_data_type(args.data_type, args.parent_type)
    elif args.delete:
        if args.data_id:
            data.del_data(args.data_id)
        elif args.data_type:
            data.del_data_type(args.data_type)
    elif args.get:
        if args.data_id:
            print(data.get_data_description(args.data_id))
        elif args.data_type:
            print(data.get_datatype_description(args.data_type))
        else:
            print(data.get_all_items())
    elif args.upload_data:
        print(data.upload_data_for_type(args.upload_data, args.data_type))
    elif args.save_metadata and args.data_id:
        with open(args.save_metadata) as dfile:
            jsonobj = json.load(dfile)
            data.save_metadata(args.data_id, jsonobj)
    elif args.data_location and args.data_id:
        data.set_data_location(args.data_id, args.data_location)
    elif args.add_properties and args.data_type:
        with open(args.add_properties) as dfile:
            jsonobj = json.load(dfile)
            data.add_type_properties(args.data_type, jsonobj)

    # Logout
    data.logout()
