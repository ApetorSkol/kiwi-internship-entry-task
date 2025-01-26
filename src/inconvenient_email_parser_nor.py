# Kiwi internship task
# Author: Matej Slivka
# May 2022

# # # # # # # # # # # # # # # # # # # # 
# This module parser emails which contain information about flight changes.
# Using regexes, this module parses information about airports, flights, carrier and returns them in json dictionary
# Module works with emails that are all same formated, with different types of data
# regexes were empiricaly created to fit emails
# # # # # # # # # # # # # # # # # # # # 

from bs4 import BeautifulSoup   # for parsing html
import re                       # regex
import json                     # json 
from datetime import datetime   # datetime

# this function returns information extracted from flights
def extract_flights(text):
    # create regex which gives us information about flight
    flight_re = re.compile(r"""ARRIVAL  
                                \s*                              
                                (?P<dep_airport>[a-zA-z -]+)
                                \s*
                                [(]
                                (?P<dep_iata>[A-Z]+)
                                [)]
                                \s*
                                (?P<arr_airport>[a-zA-z -]+)
                                \s*
                                [(]
                                (?P<arr_iata>[A-Z]+)
                                [)]  
                                \s*
                                (?P<carrier>[A-Z]+)
                                (?P<carrier_num>[0-9]+)
                                \s*
                                (?P<dep_time_d_m_y>[a-zA-Z0-9]+)
                                \s*
                                (?P<dep_time_h_min>[:0-9]+)
                                \s*
                                (?P<arr_time_d_m_y>[a-zA-Z0-9]+)
                                \s*
                                (?P<arr_time_h_min>[:0-9]+)
                                """, re.X)     
    
    flights = flight_re.finditer(text)
    if not flights:
        return {}
    
    output = []
    
    # create dictionary which returns found data
    for iter in flights:
        departure = {
            "airport": iter.group('dep_airport'),
            "airport_iata": iter.group('dep_iata'),
            "datetime": datetime.strptime(iter.group("dep_time_d_m_y") + iter.group("dep_time_h_min"),  "%d%b%Y%H:%M").__repr__(),
        }
        arrival = {
            "airport": iter.group('arr_airport'),
            "airport_iata": iter.group('arr_iata'),
            "datetime": datetime.strptime(iter.group("arr_time_d_m_y") + iter.group("arr_time_h_min"),  "%d%b%Y%H:%M").__repr__(),
        }
        flight_dict ={
            "carrier": iter.group('carrier'),
            "carrier_number": iter.group('carrier_num'),
            "departure": departure,
            "arrival": arrival,
        }
        output.append(flight_dict)
    
    return output

# function called from main
def nor_parser(text):

    # create regex which would give us only flights which are old
    # These flights are after "Old flight" and before "New flight" in text
    old_flights_re = re.compile(r"""Old[ ]flight
                                .*              
                                New[ ]flight     
                                    """, re.X | re.DOTALL)
    if not old_flights_re.search(text):
        exit()
    old_flights_text = old_flights_re.search(text).group(0)

    # create regex which would give us only flights which are new
    # These flights are after "New flight" in text
    new_flights_re = re.compile(r"""New[ ]flight
                                .*                   
                                    """, re.X | re.DOTALL)
    if not new_flights_re.search(text):
        exit()
    new_flights_text = new_flights_re.search(text).group(0)

    # check file for reservation number
    reservation_re = re.compile(r"""Booking[ ]Reference:
                                (\s)*
                                (?P<reservation_num>\S+)
                                """, re.X )
    if not reservation_re.search(text):
        exit()
    
    reservation_text = reservation_re.search(text).group('reservation_num')

    # create output
    final_output = {
        "reservation_number": reservation_text,
        "old_flights": extract_flights(old_flights_text),
        "new_flights": extract_flights(new_flights_text),
    }
    
    return json.dumps(final_output,indent=4,default=str)