import csv
import argparse
import wings.domain

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument("-u", "--userid", help="Portal userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal password", default="4dm1n!23")
parser.add_argument("-d", "--domain", help="Domain to get details for")
parser.add_argument("-i", "--import_domain", help="Import domain URL")
parser.add_argument("-dl", "--domain_list", help="Import domain CSV File")
args = parser.parse_args()

# Create manage domain api
domain = wings.ManageDomain(args.server, args.userid)

# Login with password
if domain.login(args.password):
    if args.domain:
        print domain.get_domain_details(args.domain)
    elif args.import_domain:
        domain.import_domain(args.import_domain)
    elif args.domain_list:
        with open(args.domain_list, 'rb') as csvfile:
            fdata = csv.reader(csvfile)
            for row in fdata:
                domainurl = row[0]
                print "importing from %s" % domainurl
                domain.import_domain(domainurl)
    # Logout
    domain.logout()
else:
    print "Could not login %s:%s @%s" % (args.userid, args.password, args.server)
