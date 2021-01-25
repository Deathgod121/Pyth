import time
import psycopg2
from datetime import datetime
import os
import sys
#import map_tracker
import re

############################################################
############################################################
#######################  FUNCTIONS #########################
def get_no_of_maps_completed(data_dict):
    try:
        no_of_maps = 0
        for value in data_dict.keys():
            no_of_maps = no_of_maps + 1

        return no_of_maps

    except Exception as e:
        print("\nAn error has occured getting number of maps: %s" % e)
        return "error"
#######################  FUNCTIONS #########################
############################################################
############################################################

####################### MAIN BLOCK #########################
############################################################
############################################################
def loop_dashboard(path_dir, char_name):
    print("HERE")
    time.sleep(2)

    data_dict  = build_data_dictionary(path_dir)
    if data_dict == "no_file" and data_dict == "error":
        check_if_quit("quit")

    while True:
        refresh_interval = input("Please enter your desired refresh interval in seconds: ")
        if refresh_interval.isdigit():
            refresh_interval = int(refresh_interval)
            os.system('cls' if os.name == 'nt' else 'clear')
            break

    counter = 0
    while True:
        counter = counter + 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("#############################################################################################################################################################################################################################################")
        #print("#############################################################################################################################################################################################################################################")
        print("Player Name: %s ##### Current Lvl: %s ##### "+"%"+" of Lvl Completed %s" % (char_name, 1, 2))
        
        time.sleep(refresh_interval)

    ####################### MAIN BLOCK #########################
    ############################################################
    ############################################################

"""
loop_count =  0
while True:
    loop_count = loop_count + 1

    print("Yes im looping: %s" % loop_count)
    time.sleep(2)

    if loop_count > 10:
        break
"""