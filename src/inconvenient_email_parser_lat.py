# Kiwi internship task
# Author: Matej Slivka
# May 2022

# # # # # # # # # # # # # # # # # # # # 
# This module parser emails which contain information about flight changes.
# Using regexes, this module parses information about airports, flights, carrier and returns them in json dictionary
# Module works with emails that are all same formated, with different types of data
# regexes were empiricaly created created to fit emails
# # # # # # # # # # # # # # # # # # # # 

from bs4 import BeautifulSoup               # for parsing html
import re                                   # regex
import json                                 # json 
from datetime import datetime               # work with datetime
from datetime import timedelta as timedelta # 

# this function returns output for delayed flights
def extract_flights_delay(text, airport):
    # create regex for data extraction from email
    flight_re = re.compile(r"""((Original[ ]itinerary)|(Cancelled[ ]Flight)|(New[ ]itinerary)|(Suggested[ ]Flight)) 
                                (\s)*
                                (?P<carrier>[A-Z]+)
                                (?P<carrier_num>[0-9]+)
                                (\s)*
                                (?P<dep_time_m>[a-zA-Z ]+)
                                (?P<dep_time_d>[0-9 ]+)
                                \D*
                                (?P<dep_time_y>[0-9]+)
                                \s*
                                (?P<dep_time_h_min>[:0-9]+)
                                \s*                                                            
                                (?P<dep_iata>[A-Z]+)
                                (?P<arr_time_h_min>[:0-9]+)
                                \s*
                                (?P<day_diff>[\+\-\d]*)
                                \s*
                                (?P<arr_iata>[A-Z]+)
                                """, re.X)     
    
    flights = flight_re.finditer(text)
    if not flights:
        return {}
    
    return get_output(flights,airport)


# this function returns output for cancelled flights
def extract_flights_cancel(text, airport):
    # create regex for data extraction from email
    flight_re = re.compile(r"""((Original[ ]itinerary)|(Cancelled[ ]Flight)|(New[ ]itinerary)|(Suggested[ ]Flight)) 
                                (\s)*
                                (?P<carrier>[A-Z]+)
                                (?P<carrier_num>[0-9]+)
                                (\s)*
                                (?P<dep_time_m>[a-zA-Z ]+)
                                (?P<dep_time_d>[0-9 ]+)
                                \D*
                                (?P<dep_time_y>[0-9]+)
                                \s*
                                (?P<dep_time_h_min>[:0-9]+)
                                \s*                 
                                (?P<dep_iata>[A-Z]+)
                                \s*
                                (?P<arr_iata>[A-Z]+)
                                """, re.X)     
    

    flights = flight_re.finditer(text)
    if not flights:
        return {}
    
    return get_output(flights,airport)

# function returns parsed data from old and new flights
def get_output(flights,airport):
    output = []
    
    for iter in flights:
        # create departure
        departure = {
            "airport": airport["origin"],
            "airport_iata": iter.group('dep_iata'),
            # convert datetime
            "datetime": datetime.strptime(iter.group("dep_time_m")+iter.group("dep_time_d")+" "+iter.group("dep_time_y")+" "+iter.group("dep_time_h_min"), "%B %d %Y %H:%M").__repr__(),
        }
        # create arrival
        # if arr_time is specified, then function parses "delay" flights
        try:
            # if there is day diff , then calculate correct date
            iter.group('arr_time_h_min')
            if iter.group('day_diff'):
                time = datetime.strptime(iter.group("dep_time_m")+iter.group("dep_time_d")+" "+iter.group("dep_time_y")+" "+iter.group("arr_time_h_min"), "%B %d %Y %H:%M")
                one_day= timedelta(hours=24)
                if iter.group('day_diff')[0] == "+":
                    time = time + one_day*int(iter.group('day_diff')[0:])
                else :
                    time = time - one_day*int(iter.group('day_diff')[0:])
                arrival = {
                    "airport": airport["destination"],
                    "airport_iata": iter.group('arr_iata'),
                    "datetime":time,
                }
            # if there is not day diff , then calculate date time
            else:
                arrival = {
                    "airport": airport["destination"],
                    "airport_iata": iter.group('arr_iata'),
                    "datetime":datetime.strptime(iter.group("dep_time_m")+iter.group("dep_time_d")+" "+iter.group("dep_time_y")+" "+iter.group("arr_time_h_min"), "%B %d %Y %H:%M"),
                }
        except:
            # if arr_time is not specified, then  function parser cancel flights
            arrival = {
                "airport": airport["destination"],
                "airport_iata": iter.group('arr_iata'),
                "datetime": "",
            }

        # create dict for output
        flight_dict ={
            "carrier": iter.group('carrier'),
            "carrier_number": iter.group('carrier_num'),
            "departure": departure,
            "arrival": arrival,
        }
        output.append(flight_dict)
    return output

# this function searches text for name of cities
# cities are used instead of airport names since airports are not defined
def return_cities(text):
    flight_re = re.compile(r"""your\sflight\sfrom\s 
                            (?P<origin>[\w ]+)
                            to\s
                            (?P<destination>[^\.]+)
                            \.
                            """, re.X)     
    
    flights = flight_re.search(text)
    if not flights:
        return {"destination": "",
                "origin": ""}

    output = {
        "destination": flights.group("destination"),
        "origin": flights.group("origin")[:-1]
        }
    return output

# this function is called from main
def lat_parser(text):

    # create regex which returns only old flight
    old_flights_re = re.compile(r"""((Original[ ]itinerary)|(Cancelled[ ]Flight))
                                .*              
                                ((New[ ]itinerary)|(Suggested[ ]Flight)) 
                                    """, re.X | re.DOTALL)
    if not old_flights_re.search(text):
        exit()
    old_flights_text = old_flights_re.search(text).group(0)

    # create regex which returns only new flight
    new_flights_re = re.compile(r"""((New[ ]itinerary)|(Suggested[ ]Flight)) 
                                .*                   
                                    """, re.X | re.DOTALL)
    if not new_flights_re.search(text):
        exit()
    new_flights_text = new_flights_re.search(text).group(0)

    # since we dont know which airports is client flying from, then airports are represented as cities , from which are clients flying
    airports = return_cities(text)

    # if text contains delay, then call function for extracting data from delay email
    # else call function for extracting data from cancel emal
    delay_re = re.compile(r"""delay""", re.X)
    if delay_re.search(text):
        final_output = {
            # NOTE : I could not find reservation number in any of those emails
            "reservation_number": "",
            "old_flights": extract_flights_delay(old_flights_text, airports),
            "new_flights": extract_flights_delay(new_flights_text, airports),  
        }
    else:
        final_output = {
            "reservation_number": "",
            "old_flights": extract_flights_cancel(old_flights_text, airports),
            "new_flights": extract_flights_cancel(new_flights_text, airports),  
        }
    return json.dumps(final_output,indent=4,default=str)