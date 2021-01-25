import time
import psycopg2
from datetime import datetime
import os
import sys

############################################################
############################################################
#######################  FUNCTIONS  ########################
def build_data_dictionary(path_dir):
    try:
        log_file = False
        if os.path.exists(path_dir):
            log_file = open(path_dir, "r")
            key_no    = 0
            data_dict = {}

            for line in log_file:
                if line[:2] != "--":
                    data_dict[key_no] = line[31:]
                    key_no            = key_no + 1
            
            return data_dict
        else:
            print("\nNo path file found at %s" % path_dir)
            return "no_file"

    except Exception as e:
        print("\nAn error has occured building data dictionary: %s" % e)
        return "error"

    finally:
        if log_file:
            log_file.close()
#############################################################

def check_if_quit(input_value):
    if input_value.lower() == "quit":
        sys.exit(0)
#############################################################

def select_char(path_dir):
    try:
        print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        char_name_list = []
        all_files      = [f for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]

        for check in all_files:
            if ".path" in check:
                print("Found the following exisiting character(s):")
                break

        all_files.sort()
        count    = 0
        existing = False
        for pfile in all_files:
            if ".path" in pfile:
                count    = count + 1
                existing = True
                char_name_list.append(pfile.lower()[:pfile.index(".path")])
                print("%s: %s" % (count, pfile[:pfile.index(".path")]))
                  
        if existing:
            response = input("\nInput number or type in name (New names will get a new file): ")
            check_if_quit(response)
        else:
            response = input("No Existing character files found. Start a new file for: ")
            if response == "":
                response = input("Please enter a character name: ")
            check_if_quit(response)

        while True:
            if response.isdigit() and existing:
                if int(response) < 0 or int(response) > count:
                    response = input("Please only enter numbers between 1 and %s: " % count)
                    check_if_quit(response)
                else:
                    response = int(response) - 1
                    selected_char = char_name_list[response]
                    print("Using character file for: %s.\n" % selected_char)
                    return selected_char
            else:
                if response in char_name_list:
                    print("Using character file for: %s.\n" % response)
                    return response
                else:
                    if response == "":
                        response = input("Please enter a character name: ")
                        check_if_quit(response)
                    else:
                        print("Stating new character file for %s...\n" % response)
                        return response

    except Exception as e:
        print("\nPrint an error has occured selecting character %s" % e)
        time.sleep(10)
        return "p12xp45" # Incase you named your char error
#############################################################

def link_path_file(path_dir, input_value):
    try:
        check_if_quit(input_value)

        while True:
            if input_value == "c" or input_value == "r" or input_value == "b":
                break
            else:
                input_value = input("Please only select c, r or b: ").lower()
                check_if_quit(input_value)

        if os.path.exists(path_dir):
            print("")
            if input_value == "r":
                print("Clearing existing log at %s.\n" % path_dir)
                path_log_file = open(path_dir, "w")  ## REMEBER TO CLOSE FILE!
                path_log_file.close()
                path_log_file = open(path_dir, "a")  ## REMEBER TO CLOSE FILE!

            elif input_value == "b":
                backup_file = path_dir.replace(".path","_"+str(datetime.today()).replace(" ","_").replace(":","-")[:16])+".pbck"
                print("Renaming old log to %s. Creating a new log at %s\n" % (backup_file, path_dir))
                os.rename(path_dir,backup_file)
                path_log_file = open(path_dir, "w")  ## REMEBER TO CLOSE FILE! 
                path_log_file.close()  ## REMEBER TO CLOSE FILE! 
                path_log_file = open(path_dir, "a")  ## REMEBER TO CLOSE FILE!

            elif input_value == "c":
                print("Extending existing log at %s\n" % path_dir)
                path_log_file = open(path_dir, "a")  ## REMEBER TO CLOSE FILE!
            
        else:
            print("No existing log found. Creating new file at %s\n" % path_dir)
            path_log_file = open(path_dir, "w")  ## REMEBER TO CLOSE FILE! 
            path_log_file.close()  ## REMEBER TO CLOSE FILE! 
            path_log_file = open(path_dir, "a")  ## REMEBER TO CLOSE FILE!

        print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        return path_log_file

    except Exception as e:
        print("\nAn error has occured linking path file: %s" % e)
        return "error"
#############################################################

def validate_current_xp(xp):
    if xp == "quit":
        check_if_quit("quit")

    while True:
        if xp.isdigit():
            return xp
        else:
            xp = input("Please only enter numbers. Please enter your current XP: ")
            if xp == "quit":
                check_if_quit("quit")
#############################################################

def get_current_lvl(xp):
    lvls_dict = {
        1   : 0,
        2   : 525,
        3   : 1760,
        4   : 3781,
        5   : 7184,
        6   : 12186,
        7   : 19324,
        8   : 29377,
        9   : 43181,
        10  : 61693,
        11  : 85990,
        12  : 117506,
        13  : 157384,
        14  : 207736,
        15  : 269997,
        16  : 346462,
        17  : 439268,
        18  : 551295,
        19  : 685171,
        20  : 843709,
        21  : 1030734,
        22  : 1249629,
        23  : 1504995,
        24  : 1800847,
        25  : 2142652,
        26  : 2535122,
        27  : 2984677,
        28  : 3496798,
        29  : 4080655,
        30  : 4742836,
        31  : 5490247,
        32  : 6334393,
        33  : 7283446,
        34  : 8384398,
        35  : 9541110,
        36  : 10874351,
        37  : 12361842,
        38  : 14018289,
        39  : 15859432,
        40  : 17905634,
        41  : 20171471,
        42  : 22679999,
        43  : 25456123,
        44  : 28517857,
        45  : 31897771,
        46  : 35621447,
        47  : 39721017,
        48  : 44225461,
        49  : 49176560,
        50  : 54607467,
        51  : 60565335,
        52  : 67094245,
        53  : 74247659,
        54  : 82075627,
        55  : 90631041,
        56  : 99984974,
        57  : 110197515,
        58  : 121340161,
        59  : 133497202,
        60  : 146749362,
        61  : 161191120,
        62  : 176922628,
        63  : 194049893,
        64  : 212684946,
        65  : 232956711,
        66  : 255001620,
        67  : 278952403,
        68  : 304972236,
        69  : 333233648,
        70  : 363906163,
        71  : 397194041,
        72  : 433312945,
        73  : 472476370,
        74  : 514937180,
        75  : 560961898,
        76  : 610815862,
        77  : 664824416,
        78  : 723298169,
        79  : 786612664,
        80  : 855129128,
        81  : 929261318,
        82  : 1009443795,
        83  : 1096169525,
        84  : 1189918242,
        85  : 1291270350,
        86  : 1400795257,
        87  : 1519130326,
        88  : 1646943474,
        89  : 1784977296,
        90  : 1934009687,
        91  : 2094900291,
        92  : 2268549086,
        93  : 2455921256,
        94  : 2658074992,
        95  : 2876116901,
        96  : 3111280300,
        97  : 3364828162,
        98  : 3638186694,
        99  : 3932818530,
        100 : 4250334444
    }

    for key, value in lvls_dict.items():
        if int(xp) >=  value:
            current_lvl = key
        
        if int(xp) < value:
            return current_lvl
#############################################################

def get_xp_to_level(current_lvl):
    lvls_dict = {
        1   : 0,
        2   : 525,
        3   : 1760,
        4   : 3781,
        5   : 7184,
        6   : 12186,
        7   : 19324,
        8   : 29377,
        9   : 43181,
        10  : 61693,
        11  : 85990,
        12  : 117506,
        13  : 157384,
        14  : 207736,
        15  : 269997,
        16  : 346462,
        17  : 439268,
        18  : 551295,
        19  : 685171,
        20  : 843709,
        21  : 1030734,
        22  : 1249629,
        23  : 1504995,
        24  : 1800847,
        25  : 2142652,
        26  : 2535122,
        27  : 2984677,
        28  : 3496798,
        29  : 4080655,
        30  : 4742836,
        31  : 5490247,
        32  : 6334393,
        33  : 7283446,
        34  : 8384398,
        35  : 9541110,
        36  : 10874351,
        37  : 12361842,
        38  : 14018289,
        39  : 15859432,
        40  : 17905634,
        41  : 20171471,
        42  : 22679999,
        43  : 25456123,
        44  : 28517857,
        45  : 31897771,
        46  : 35621447,
        47  : 39721017,
        48  : 44225461,
        49  : 49176560,
        50  : 54607467,
        51  : 60565335,
        52  : 67094245,
        53  : 74247659,
        54  : 82075627,
        55  : 90631041,
        56  : 99984974,
        57  : 110197515,
        58  : 121340161,
        59  : 133497202,
        60  : 146749362,
        61  : 161191120,
        62  : 176922628,
        63  : 194049893,
        64  : 212684946,
        65  : 232956711,
        66  : 255001620,
        67  : 278952403,
        68  : 304972236,
        69  : 333233648,
        70  : 363906163,
        71  : 397194041,
        72  : 433312945,
        73  : 472476370,
        74  : 514937180,
        75  : 560961898,
        76  : 610815862,
        77  : 664824416,
        78  : 723298169,
        79  : 786612664,
        80  : 855129128,
        81  : 929261318,
        82  : 1009443795,
        83  : 1096169525,
        84  : 1189918242,
        85  : 1291270350,
        86  : 1400795257,
        87  : 1519130326,
        88  : 1646943474,
        89  : 1784977296,
        90  : 1934009687,
        91  : 2094900291,
        92  : 2268549086,
        93  : 2455921256,
        94  : 2658074992,
        95  : 2876116901,
        96  : 3111280300,
        97  : 3364828162,
        98  : 3638186694,
        99  : 3932818530,
        100 : 4250334444
    }

    current_lvl = current_lvl + 1
    return int(lvls_dict[current_lvl])


def validate_map_tier(tier):
    if tier == "quit":
        check_if_quit("quit")

    while True:
        if tier.isdigit():
            if int(tier) > 0 and int(tier) < 20:
                return tier
            else:
                tier = input("Enter the map tier (Only numbers 1-19): ")
                if tier == "quit":
                    check_if_quit("quit")
        else:
            tier = input("Enter the map tier (Only numbers 1-19): ")
            if tier == "quit":
                check_if_quit("quit")
#############################################################

def validate_map_name(name):
    if name == "quit":
        check_if_quit("quit")

    while True:
        if name.isalpha():
            return name
        else:
            name = input("Enter the map name (Only letters please): ")
#############################################################

def calculate_map_time():
    print("\nReady to start map! Hit enter to start.")
    input("-----------------------------------------")
    total_time_taken = 0
    start_time       = datetime.today()

    while True:
        input("\nRun map. Hit enter to pause.")
        end_time         = datetime.today()
        time_taken       = 0
        time_taken       = (end_time - start_time).total_seconds()
        total_time_taken = total_time_taken + time_taken

        print("\n-------")
        print("PAUSED!")
        print("-------\n")

        pause_option = input("Would you like to (c)ontinue or (f)inish the map or (a)bandon the map: ").lower()
        check_if_quit(pause_option)
        while True:
            if pause_option == "c" or pause_option == "f" or pause_option == "a":
                break
            else:
                pause_option = input("Invalid selection. Would you like to (c)ontinue or (f)inish the map or (a)bandon the map: ").lower()
        print("")
        start_time = datetime.today()

        if pause_option == "f":
            return int(total_time_taken)
        
        elif pause_option == "a":
            return "aban"
#############################################################  

def check_lvl_up(current_xp, new_xp):
    current_lvl = get_current_lvl(current_xp)
    new_lvl     = get_current_lvl(new_xp)
    if current_lvl != new_lvl:
        return True
    else:
        return False
#############################################################  

def validate_deaths(deaths):
    if deaths == "quit":
        check_if_quit("quit")
    
    while True:
        if deaths.isdigit():
            if int(deaths) > 0:
                print("Offff. That Cost you %s" % (str(int(deaths) * 10))+"%" + " XP...")
                return deaths
            else:
                return deaths
        else:
            deaths = input("Please only enter numbers: ")
            check_if_quit(deaths)
#######################  FUNCTIONS  ########################        
#############################################################
############################################################

       
############################################################
############################################################
#######################  DASHBOARD  ########################
def get_no_of_maps_completed(data_dict):
    try:
        no_of_maps = 0
        for value in data_dict.keys():
            no_of_maps = no_of_maps + 1

        return no_of_maps

    except Exception as e:
        print("\nAn error has occured getting number of maps: %s" % e)
        return "error"

def calc_current_lvl(data_dict):

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()

    return current_lvl
############################################################    

def calc_perc_of_lvl(data_dict):
    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

    xp_for_current_lvl = get_xp_to_level(int(current_lvl) - 1)
    next_level_xp      = get_xp_to_level(int(current_lvl))
    total_xp_for_lvl   = next_level_xp - xp_for_current_lvl
    xp_for_this_lvl    = int(current_xp) - xp_for_current_lvl

    return round((xp_for_this_lvl * 100) / total_xp_for_lvl,2)
############################################################    

def calc_no_of_deaths(data_dict):
    total_deaths = 0

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        total_deaths = total_deaths + int(deaths)
    
    return total_deaths
############################################################        

def calc_no_of_lvl_ups(data_dict):
    total_lvl_ups = 0

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        if lvld_up.lower() == "true":
            total_lvl_ups = total_lvl_ups + 1
    
    return total_lvl_ups
############################################################ 

def calc_xp_gained(data_dict):
    total_xp_gained = 0

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        total_xp_gained = total_xp_gained + int(xp_gained)
    
    return total_xp_gained
############################################################ 

def calc_xp_perc_lost(data_dict):
    total_deaths = 0

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        total_deaths = total_deaths + int(deaths)
    
    return str(int(total_deaths) * 10)
############################################################ 

def calc_most_xp_gain(data_dict):
    highest_xp = 0
    map_name   = ""

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        if int(xp_gained) > int(highest_xp):
            highest_xp = xp_gained
            map_name   = "T" + tier 
            map_name   = map_name.ljust(3," ") + " --> " + name + " (%s)" % highest_xp
    
    return map_name
############################################################ 

def calc_quickest_map(data_dict):
    least_time_taken = 99999999999999999
    map_name         = ""

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        if int(time_taken) < int(least_time_taken):
            least_time_taken = time_taken
            map_tier         = tier
            use_map_name     = name

    map_name   = "T" + map_tier 
    map_name   = map_name.ljust(3," ") + " --> " + use_map_name #+ " (%s)" % least_time_taken

    if int(least_time_taken) >= 60:
        least_time_taken   = int(least_time_taken)
        minutes_calc = str(least_time_taken / 60)
        minutes      = minutes_calc[:minutes_calc.index(".")]
        seconds      = least_time_taken % 60

        map_name = map_name + " (%s minutes and %s seconds)" % (minutes, seconds)
    else:
        map_name = map_name + " (%s seconds)" % least_time_taken
    
    return map_name
############################################################

def calc_deadliest_map(data_dict):
    death_count_per_map_dict = {}

    for key, value in data_dict.items():
        line        = str(value)
        current_lvl = line[:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        tier        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        name        = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        time_taken  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        current_xp  = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        xp_gained   = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        lvld_up     = line[0:line.index("|")].strip()
        line        = line[line.index("|")+1:]
        deaths      = line[0:].strip()

        if int(deaths) > 0:
            if name in death_count_per_map_dict:
                curr_deaths = death_count_per_map_dict[name]
                curr_deaths = int(curr_deaths) + int(deaths)
                death_count_per_map_dict.pop(name)
                death_count_per_map_dict[name] = curr_deaths
            else:
                death_count_per_map_dict[name] = deaths
        
    most_deaths = 0
    for key, value in death_count_per_map_dict.items():
        if int(value) > int(most_deaths):
            map_name   = "T" + tier 
            map_name   = map_name.ljust(3," ") + " --> " + key + " (%s)" % value
            most_deaths = value 
    
    return map_name
############################################################

def loop_dashboard(path_dir,char_name):
    while True:
        data_dict = build_data_dictionary(path_dir)

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
            data_dict = build_data_dictionary(path_dir)
            counter = counter + 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CTRL + C --> Quit Dashboard!" )
            print("")
            print("############### PLAYER ######################################################################################################################################################################################################################")
            print("")
            #print("#############################################################################################################################################################################################################################################")
            print("Player Name:         %s" % char_name)
            print("Current Level:       %s" % calc_current_lvl(data_dict))
            print("%% of lvl completed:  %s%%" % calc_perc_of_lvl(data_dict))
            print("")
            print("############### STATS #####################################################################################################################################################################################################################")
            print("")
            print("Total number of tracked maps completed: %s" % get_no_of_maps_completed(data_dict))
            print("Total number of tracked deaths:         %s" % calc_no_of_deaths(data_dict))
            print("Total number of tracked lvl ups:        %s" % calc_no_of_lvl_ups(data_dict))
            print("")
            print("")
            print("############### XP ########################################################################################################################################################################################################################")
            print("")
            print("Total tracked XP gained:    %s" % calc_xp_gained(data_dict))
            print("Total tracked %% of XP lost: %s%%" % calc_xp_perc_lost(data_dict))
            print("")
            print("")
            print("############### MAPS ######################################################################################################################################################################################################################")
            print("")
            print("Map with most XP gained: %s" % calc_most_xp_gain(data_dict))
            print("Quickest completed map:  %s" % calc_quickest_map(data_dict))
            print("Deadliest map:           %s" % calc_deadliest_map(data_dict))
            print("")
            print("")
            print("#############################################################################################################################################################################################################################################")
            #+"%"+" of Lvl Completed %s" % (char_name, char_name, "", char_name))
            
            time.sleep(refresh_interval)
#######################  DASHBOARD  ######################## 
############################################################
############################################################       


#############################################################
#############################################################
#######################  MAIN BLOCK  ########################
def main_block(process_type):
    

    print("Run me in full screen mode (1080x1920) :P")
    print('Type "quit" at any input section to quit.')
    print('If your XP changes outside of map please reset application.')

    try:
        ### Start job and check if path exists
        path_dir = sys.argv[1]
        path_dir = path_dir.replace("\\","/")
        if path_dir[-1] == "\\" or path_dir[-1] == "/":
            None
        else:
            path_dir += "/"

        if os.path.exists(path_dir):
            None
        else:
            print("\nThe following path does not exist, please create it: %s" % path_dir) 
            check_if_quit("quit")

        ### Select character file to use
        char_name = select_char(path_dir)
        if char_name == "p12xp45": # Incase you named your char error
            check_if_quit("quit")

        ### Set file to use
        path_dir = path_dir + "%s.path" % char_name.lower()

        ## Skip this for the dash
        if process_type != "dash":
            ### Link log file
            path_log_file = link_path_file(path_dir, input("Do you want to (c)ontinue file or (r)eset file or (b)ackup old file and reset file :"))
            if path_log_file == "error":
                check_if_quit("quit")

            ### Build data dict to use
            data_dict  = build_data_dictionary(path_dir)
            if data_dict == "no_file" and data_dict == "error":
                check_if_quit("quit") 

        if process_type == "dash":
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                loop_dashboard(path_dir, char_name)
            except Exception as e:
                print("Error: %s" % e)
                time.sleep(100)
            print("AFTER")
            time.sleep(10)
            return "done"

        print("-- ",str(datetime.today()), "--> Starting XP tracker." ,file=path_log_file,flush=True)
        print("-- ",str(datetime.today()), "--> String Mask = current_lvl|tier|map|time_taken|xp_gained|lvld_up|deaths." ,file=path_log_file,flush=True)

        ### Validate current XP and get current lvl
        while True:
            current_xp  = validate_current_xp(input("Please enter your current XP: "))
            current_lvl = get_current_lvl(current_xp)
            response = input("Your current lvl is: %s. Is this correct (Y/N): " % current_lvl)
            check_if_quit(response)
            if response.lower() == "y":
                break
            elif response.lower() == "n":
                None         

        ### Clear the screen to focus on maps
        os.system('cls' if os.name == 'nt' else 'clear')

        ### Main Loop for getting information
        while True:
            print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            current_tier = validate_map_tier(input("Enter the map tier: "))
            current_map  = validate_map_name(input("Enter the map name: "))

            time_taken   = calculate_map_time()
            if time_taken != "aban": ## if we not tracking this map then reset.

                ### Calculate XP gained
                new_xp     = validate_current_xp(input("Please enter your current XP: "))
                xp_gained  = int(new_xp) - int(current_xp)

                ### Check if we lvld up
                lvld_up     = check_lvl_up(current_xp, new_xp)

                ### Get current level
                current_lvl = get_current_lvl(new_xp)

                ### Set the new current XP
                current_xp = new_xp

                ### Death counter
                deaths = validate_deaths(input("How many times did you die: "))

                ### Log to file
                while True:
                    log_to_file = input("Log run to path file? (Y/N): ").lower()
                    check_if_quit(log_to_file)

                    if log_to_file == "y":
                        if int(time_taken) >= 60:
                            time_taken   = int(time_taken)
                            minutes_calc = str(time_taken / 60)
                            minutes      = minutes_calc[:minutes_calc.index(".")]
                            seconds      = time_taken % 60

                            print("\nMap completed in %s minutes and %s seconds. Map logged. Next!" % (minutes, seconds))
                            print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                        else:
                            print("\nMap completed in %s seconds and logged. Next!" % int(time_taken))
                            print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                        
                        ### Log details to the file
                        print(str(datetime.today()), "--> %s|%s|%s|%s|%s|%s|%s|%s" % (current_lvl, current_tier, current_map, time_taken, current_xp, xp_gained, lvld_up, deaths) ,file=path_log_file,flush=True)
                        break

                    elif log_to_file == "n":
                        print("\nMap not logged. Next!")
                        break

                    else:
                        print("Invalid selection. Log run to path file? (Y/N): ")

            ### keep all logic in this if, to decide if we tracking it.       
            else:
                print("Current map abandoned. Stats not tracked.\n")

    except Exception as e:
        print("\nAn error has occured: %s" % e)

    finally:
        if process_type == "map":
            input("\nQuitting application. Press enter to quit application.")

        if path_log_file:
            path_log_file.close()

#######################  MAIN BLOCK  ########################
#############################################################
#############################################################



#######################  DASH OR MAP  ########################
dash_or_map = sys.argv[2]

if dash_or_map == "map":
    main_block("map")
elif dash_or_map == "dash":
    main_block("dash")
else:
    print("2nd Arg not map/dash. Closing in 5 seconds.")
    time.sleep(5)

#######################  DASH OR MAP  ########################    