# Kiwi internship task
# Author: Matej Slivka
# May 2022

# # # # # # # # # # # # # # # # # # # # 
# This module chceks arguments and calls parsing functions acordingly
# If 1 argument is specified then this scipt prints output to stdout
# If no argument is specified then this scipt runs as web Flask API
# # # # # # # # # # # # # # # # # # # # 



import inconvenient_email_parser_nor as nor
import inconvenient_email_parser_lat as lat

import argparse                             # for working with arguments
from bs4 import BeautifulSoup               # for parsing html
import re                                   # regex
from flask import Flask, request ,jsonify   # creating flask API
import sys                                  # for stderr

# create instance of class
app = Flask(__name__)

# method "parse" - which responds to request
# if this method is called then given html text is parsed
# if there is no html text then function returns {}
@app.route('/parse/', methods=['GET', 'POST'])
def parse_request():
    text = BeautifulSoup(request.get_data(), 'html.parser').get_text()
    return call_airline_parser(text)

# this function determines whether given HTML file is about LATAM or about Norwegian Air Shuttle
# function calls HTML parser accordingly
# function returns dictionary with given information
def call_airline_parser(text):
    key_latam_word = re.compile(r'LATAM AIRLINES GROUP')
    key_nor_word = re.compile(r'Norwegian Air Shuttle')
    if key_latam_word.search(text):
        return lat.lat_parser(text)
    elif key_nor_word.search(text):
        return nor.nor_parser(text)
    else:
        return {}



# parse arguments. 
# only 1 argument is optional
aparser = argparse.ArgumentParser(description="Program prints information about flights from HTML file. Program uses inconvenient_email_parser_nor and inconvenient_email_parser_lat as modules. Make sure they are in same directory as this file")
aparser.add_help=True
aparser.add_argument('--file' , type=str, required=False, help="source file / email")
args = aparser.parse_args()

# argument file specifies whether this script should run as web Flask API
# or as a script which prints output
if args.file :
    try:
        with open(args.file) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        text = soup.get_text()
    except:
        sys.stderr.write("Can not open specified file.\n")
        exit()
    
    print(call_airline_parser(text))
else:
    # run this module as HTTP on adress 0 0 0 0 on port 105
    app.run(host='0.0.0.0', port=105)
