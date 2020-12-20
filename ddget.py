import dbdns
from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Reads a database and prints selected quantities on screen.")
parser.add_argument('database', help='Json file containing database.')
parser.add_argument('xdata', help='Data for x-axis. Nested dictionaries can be accessed with a slash, as in power_units/alpha.')
parser.add_argument('ydata', help='Data for y-axis. Nested dictionaries can be accessed with a slash, as in power_units/alpha.')
stg = parser.parse_args()

db_file = stg.database
xdata = stg.xdata.split('/')
ydata = stg.ydata.split('/')

db_settings = os.path.dirname(db_file) + 'dbsettings.json'

db = dbdns.dbplot(db_file, db_settings)
db.printout(xdata, ydata)