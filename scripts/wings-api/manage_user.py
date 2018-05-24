import os
import csv
import argparse
import wings.user
import wings.domain

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Wings portal server",
                    default="http://localhost:8080/wings-portal")
parser.add_argument(
    "-u", "--userid", help="Portal admin userid", default="admin")
parser.add_argument("-p", "--password",
                    help="Portal admin password", default="4dm1n!23")
parser.add_argument("-gu", "--get_user_id",
                    help="User's id to get details for")
parser.add_argument("-nu", "--new_userid", help="New user's id")
parser.add_argument("-np", "--new_password", help="New user's password")
parser.add_argument("-nn", "--new_name", help="New user's name")
parser.add_argument("-na", "--is_admin",
                    help="New user id admin", action="store_true")
parser.add_argument("-du", "--delete_userid", help="Deleting user's id")
parser.add_argument("-dl", "--delete_user_list",
                    help="Delete users from csv file")
parser.add_argument("-nl", "--new_user_list", help="Add users from csv file")
args = parser.parse_args()

# Create manage user api
user = wings.ManageUser(args.server, args.userid)

# Login with password
if user.login(args.password):
    if args.get_user_id:
        print user.get_user_details(args.get_user_id)

    elif args.new_userid and args.new_password and args.new_name:
        if user.add_user(args.new_userid):
            user.set_user_details(
                args.new_userid, args.new_password, args.new_name, args.is_admin)
        else:
            print "Could not create user: %s" % args.new_userid
    elif args.new_user_list:
        with open(args.new_user_list, 'rb') as csvfile:
            fdata = csv.reader(csvfile)
            for row in fdata:
                newuser = row[0]
                if not user.get_user_details(newuser):
                    print "Creating new user: %s" % newuser
                    if user.add_user(newuser):
                        user.set_user_details(newuser, row[1], row[2], False)
                    else:
                        print "Could not create user: %s" % newuser
                        continue
                else:
                    print "Importing domains for %s" % newuser

                if row[3]:
                    domain = wings.ManageDomain(args.server, newuser)
                    if domain.login(row[1]):
                        csvfile = os.path.dirname(
                            args.new_user_list) + '/' + row[3]
                        with open(csvfile, 'rb') as domfile:
                            domdata = csv.reader(domfile)
                            defdom = None
                            for dom in domdata:
                                domname = os.path.splitext(
                                    os.path.basename(dom[0]))[0]
                                if not domain.get_domain_details(domname):
                                    if defdom == None:
                                        defdom = domname
                                    domainurl = dom[0]
                                    print "-- importing %s from %s" % (domname, domainurl)
                                    domain.import_domain(domainurl)
                            if defdom != None:
                                domain.select_default_domain(defdom)
                                domain.delete_domain('blank')
                                domain.logout()
                    else:
                        print '%s could not login' % newuser
    elif args.delete_userid:
        user.delete_user(args.delete_userid)
    elif args.delete_user_list:
        with open(args.delete_user_list, 'rb') as csvfile:
            fdata = csv.reader(csvfile)
            for row in fdata:
                print row[0]
                user.delete_user(row[0])
    # Logout
    user.logout()
