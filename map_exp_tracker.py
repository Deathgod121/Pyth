import time
import psycopg2
from datetime import datetime
import os
import sys

"""
Work out which map is making the quickest xp for the shortest time.
and then how often you lvl up in the time. take active map time and show lvl ups per hour. and per minutes?
maybe add the ability to pause the timer when in a map but not actively playing it.
Maybe get xp amounts per lvl and use that too. Could be like this many maps per tier from a lvl based on avg.
Tiers need to be grouped then show most xp per map based on tier. like a top 10 per tier.
Anything else. Ask FC.
"""

def validate_entry(input_value, entry_type):
    if input_value.lower() == "q":
        sys.exit(0)
    
    if entry_type == "tier" or entry_type == "curr" or entry_type == "future" or entry_type == "death":
        while True:
            if input_value.isdigit():
                if entry_type == "tier":
                    if int(input_value) > 0 and int(input_value) < 19:
                        return input_value
                    else:
                        input_value = input("Enter the map tier (Only numbers 1-19): ")
                else:   
                    return input_value
            else:
                if entry_type == "tier":
                    input_value = input("Enter the map tier (Numbers only!): ")
                elif entry_type == "curr":
                    input_value = input("Enter your current xp (Numbers only!): ")
                elif entry_type == "future":
                    input_value = input("Enter your xp now (Numbers only!): ")
                elif entry_type == "death":
                    input_value = input("How many times did you die (Numbers only!): ")

    if entry_type == "name":
        while True:
            if input_value.isalpha():
                return input_value
            else:
                input_value = input("Enter the map name (No Numbers!): ").lower()
    
    if entry_type == "log" or entry_type == "lvl":
        while True:
            if input_value.lower() == "n" or input_value.lower() == "y":
                return input_value
            else:
                if entry_type == "lvl":
                    input_value = input("Did you lvl up? Only Y/N: ").lower()
                else:
                    input_value = input("Does run count (log to file)? Y/N: ").lower()


try:
    file_dir = sys.argv[1]

    file_dir = file_dir.replace("\\","/")
    if file_dir[-1] == "\\" or file_dir[-1] == "/":
        None
    else:
        file_dir += "/"

    file_dir = file_dir + "xp.path"

    print('Run me in full screen mode. I will look better :P\nInput a "q" at any point to quit.\n')

    file_choice = input("Do you want to (c)ontinue file or (r)eset file or (b)ackup old file and reset file : ").lower()
    while True:
        if file_choice == "c" or file_choice == "r" or file_choice == "b":
            break

        elif file_choice == "q":
            print("\nQuiting application!")
            input("Please enter to quit.")
            
            if xp_log_file:
                print("-- ",str(datetime.today()), "--> Stopping XP tracker." ,file=xp_log_file,flush=True)
                xp_log_file.close()
            sys.exit(0)
        else:
            file_choice = input("Please only select c, r or b: ").lower()

    if os.path.exists(file_dir):
        print("")
        if file_choice == "r":
            print("Clearing existing log at %s.\n" % file_dir)
            xp_log_file = open(file_dir, "w")  ## REMEBER TO CLOSE FILE!
            xp_log_file.close()
            xp_log_file = open(file_dir, "a")  ## REMEBER TO CLOSE FILE!

        elif file_choice == "b":
            backup_file = file_dir.replace(".path","_"+str(datetime.today()).replace(" ","_").replace(":","-")[:16])+".path"
            print("Renaming old log to %s. Creating a new log at %s\n" % (backup_file, file_dir))
            os.rename(file_dir,backup_file)
            xp_log_file = open(file_dir, "w")  ## REMEBER TO CLOSE FILE! 
            xp_log_file.close()  ## REMEBER TO CLOSE FILE! 
            xp_log_file = open(file_dir, "a")  ## REMEBER TO CLOSE FILE!

        elif file_choice == "c":
            print("Extending existing log at %s\n" % file_dir)
            xp_log_file = open(file_dir, "a")  ## REMEBER TO CLOSE FILE!
           
    else:
        print("No existing log found. Creating new file at %s\n" % file_dir)
        xp_log_file = open(file_dir, "w")  ## REMEBER TO CLOSE FILE! 
        xp_log_file.close()  ## REMEBER TO CLOSE FILE! 
        xp_log_file = open(file_dir, "a")  ## REMEBER TO CLOSE FILE! 

    print("-- ",str(datetime.today()), "--> Starting XP tracker." ,file=xp_log_file,flush=True)
    print("-- ",str(datetime.today()), "--> String Mask = tier|name|current_xp|new_xp|lvl_up|deaths|time_taken." ,file=xp_log_file,flush=True)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

    while True:
        tier       = input("Enter the map tier: ")
        tier       = validate_entry(tier, "tier")

        name       = input("Enter the map name: ").lower()
        name       = validate_entry(name, "name")

        current_xp = input("Enter your current xp: ")
        current_xp = validate_entry(current_xp, "curr")

        print("\nReady to start map! Hit enter when ready.")
        input("-----------------------------------------")
        total_time_taken = 0
        start_time = datetime.today()

        while True:
            input("\nRun map. Hit enter to pause.")
            end_time   = datetime.today()
            time_taken = 0
            time_taken = (end_time - start_time).total_seconds()
            total_time_taken = total_time_taken + time_taken 

            print("\n-------")
            print("PAUSED!")
            print("-------\n")

            pause_option = input("Would you like to (c)ontinue or (f)inish the map or (a)bandon the map: ").lower()
            while True:
                if pause_option == "c" or pause_option == "f" or pause_option == "a":
                    break
                else:
                    pause_option = input("Invalid selection. Would you like to (c)ontinue or (f)inish the map or (a)bandon the map: ").lower()
            print("")
            start_time = datetime.today()

            if pause_option == "f" or pause_option == "a":
                break
        
        if pause_option == "f":
            new_xp     = input("Enter your xp now: ")
            new_xp     = validate_entry(new_xp, "future")

            lvl_up     = input("Did you lvl up? Y/N: ").lower()
            lvl_up     = validate_entry(lvl_up, "lvl")

            deaths     = input("How many times did you die: ")
            deaths     = validate_entry(deaths, "death")

            valid      = input("Does run count (log to file)? Y/N: ").lower()
            valid      = validate_entry(valid, "log")

            if valid.lower() == "y":
                print(str(datetime.today()), "--> %s|%s|%s|%s|%s|%s|%s" % (tier, name, current_xp, new_xp, lvl_up, deaths, int(total_time_taken)) ,file=xp_log_file,flush=True)
            
                if int(total_time_taken) >= 60:
                    total_time_taken = int(total_time_taken)
                    minutes_calc = str(total_time_taken / 60)
                    minutes      = minutes_calc[:minutes_calc.index(".")]

                    seconds = total_time_taken % 60

                    print("\nMap completed in %s minutes and %s seconds. Map logged. Next!" % (minutes, seconds))
                else:
                    print("\nMap completed in %s seconds and logged. Next!" % int(total_time_taken))

            else:
                print("\nMap run ignored, not logged. Next!")

        elif pause_option == "a":
            print("\nMap run ignored, not logged. Next!")

        print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

finally:
    if xp_log_file:
        print("\nQuiting! Latest line not saved.")
        input("Please enter to quit.")
        print("-- ",str(datetime.today()), "--> Stopping XP tracker." ,file=xp_log_file,flush=True)
        xp_log_file.close()