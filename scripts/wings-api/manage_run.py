import os
import json
import argparse
import wings.run

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument("-is", "--internal_server", help="Wings internal server")
parser.add_argument(
    "-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal admin password", default="4dm1n!23")
parser.add_argument("-dom", "--domain", help="Portal domain")
parser.add_argument("-l", "--list", help="List all runs", action="store_true")
parser.add_argument("-r", "--runid", help="Get details of run")
args = parser.parse_args()

# Create manage user api
run = wings.ManageRun(args.server, args.internal_server, args.userid, args.domain)

# Login with password
if run.login(args.password):
    if args.list:
        print(run.get_all_runs());
    elif args.runid:
        print(run.get_run_details(args.runid))
    # Logout
    run.logout()
