import time
import psycopg2
from datetime import datetime
import os
import sys

"""
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
"""

########## MAIN BLOCK ##########
try:
    file_dir = sys.argv[1]

    file_dir = file_dir.replace("\\","/")
    if file_dir[-1] == "\\" or file_dir[-1] == "/":
        None
    else:
        file_dir += "/"

    file_dir = file_dir + "xp.path"

    print("Run me in full screen mode, i look better :P\n")
    input("Press enter to continue.\n")

    print_tiers = input("Show stats per map tier? (Y/N): ").lower()

    while True:
        if print_tiers.lower() == "n" or print_tiers.lower() == "y":
            break
        else:
            print_tiers = input("Show stats per map tier? Only enter (Y/N): ").lower()

    if os.path.exists(file_dir):
        ### SETUP VARIABLES ###
        tier       = 0
        name       = ""
        current_xp = 0
        new_xp     = 0
        lvl_up     = False
        deaths     = 0
        time_taken = 0

        # lt = longest_time, st = shortest_time, av = average_time, m = most, l = least, a = avg
        ### TIERS ###
        tiers       = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

        lt_per_tier      = {}
        lt_per_tier_name = {}

        st_per_tier      = {}
        st_per_tier_name = {}

        av_per_tier      = {}

        m_xp_per_tier      = {}
        m_xp_per_tier_name = {}
        l_xp_per_tier      = {}
        l_xp_per_tier_name = {}
        a_xp_per_tier      = {}

        maps_per_tier = {}
        ### TIERS ###

        ### MAPS  ###
        lt_per_map = {}
        st_per_map = {}
        av_per_map = {}

        m_xp_per_map = {}
        l_xp_per_map = {}
        a_xp_per_map = {}

        maps_per_map = {}
        ### MAPS  ###

        ### OVER  ###
        no_of_maps   = 0
        ### OVER  ###
        ### SETUP VARIABLES ###

        xp_file = open(file_dir, "r")  ## REMEBER TO CLOSE FILE! 

        for line in xp_file:
            if line[:2] != "--":
                tier = line[31:line.index("|")].strip()
                line = line[line.index("|")+1:]
                name = line[0:line.index("|")].strip()
                line = line[line.index("|")+1:]
                current_xp = line[0:line.index("|")].strip()
                line = line[line.index("|")+1:]
                new_xp = line[0:line.index("|")].strip()
                line = line[line.index("|")+1:]
                lvl_up = line[0:line.index("|")].strip()
                line = line[line.index("|")+1:]
                deaths = line[0:line.index("|")].strip()
                line = line[line.index("|")+1:]
                time_taken = line[0:].strip()

                ### Number of maps ###
                no_of_maps = no_of_maps+1

                # XP Gained
                total_gained = int(new_xp) - int(current_xp)
                
                ### Work those values ###
                ### LONGEST TIME ###
                if lt_per_tier != {}:                    
                    if tier in lt_per_tier:
                        current_time = lt_per_tier[tier]
                        last_xp      = m_xp_per_tier[tier]
                        if int(time_taken) > int(current_time):
                            lt_per_tier[tier]      = time_taken
                            lt_per_tier_name[tier] = name 
                        
                        if int(total_gained) > int(last_xp):
                            m_xp_per_tier[tier]      = total_gained
                            m_xp_per_tier_name[tier] = name

                        map_count = maps_per_tier[tier]
                        maps_per_tier[tier] = map_count+1                        

                    else:
                        lt_per_tier[tier]        = time_taken
                        lt_per_tier_name[tier]   = name
                        m_xp_per_tier[tier]      = total_gained
                        m_xp_per_tier_name[tier] = name
                        maps_per_tier[tier]      = 1
                else:
                    lt_per_tier[tier]        = time_taken
                    lt_per_tier_name[tier]   = name
                    m_xp_per_tier[tier]      = total_gained
                    m_xp_per_tier_name[tier] = name
                    maps_per_tier[tier]      = 1
                ### LONGEST TIME ###
                
                ### SHORTEST TIME ###
                if st_per_tier != {}:
                    if tier in st_per_tier:
                        current_time = st_per_tier[tier]
                        last_xp      = l_xp_per_tier[tier]
                        
                        if int(time_taken) < int(current_time):
                            st_per_tier[tier]      = time_taken
                            st_per_tier_name[tier] = name 
                        
                        if int(total_gained) < int(last_xp):
                            l_xp_per_tier[tier]      = total_gained
                            l_xp_per_tier_name[tier] = name
                        
                    else:
                        st_per_tier[tier]        = time_taken
                        st_per_tier_name[tier]   = name
                        l_xp_per_tier[tier]      = total_gained
                        l_xp_per_tier_name[tier] = name
                    
                    
                else:
                    st_per_tier[tier]        = time_taken
                    st_per_tier_name[tier]   = name
                    l_xp_per_tier[tier]      = total_gained
                    l_xp_per_tier_name[tier] = name
                
                ### SHORTEST TIME ###
                
                ### AVERAGE TIME ###
                if a_xp_per_tier != {}:
                    
                    if tier in a_xp_per_tier:
                        curr_avg_xp = a_xp_per_tier[tier]
                        curr_avg_xp = int(curr_avg_xp) * (int(maps_per_tier[tier])-1)
                        curr_avg_xp = int(curr_avg_xp) + int(total_gained)
                        curr_avg_xp = int(curr_avg_xp / int(maps_per_tier[tier]))
                        a_xp_per_tier[tier] = curr_avg_xp
                    else:
                        a_xp_per_tier[tier] = total_gained

                else:
                    a_xp_per_tier[tier] = current_xp
                ### AVERAGE TIME ###
                ### TIERS ###
                
                ### MAPS ###
                ### LONGEST TIME ###
                if lt_per_tier != {}:
                    if tier in lt_per_tier:
                        current_time = lt_per_tier[tier]
                        if int(time_taken) > int(current_time):
                            print(time_taken+" > "+current_time)
                            lt_per_tier[tier]      = time_taken
                            lt_per_tier_name[tier] = name 
                    else:
                        lt_per_tier[tier]      = time_taken
                        lt_per_tier_name[tier] = name 
                else:
                    lt_per_tier[tier]      = time_taken
                    lt_per_tier_name[tier] = name
                ### LONGEST TIME ###

                ### SHORTEST TIME ###
                if st_per_tier != {}:
                    if tier in st_per_tier:
                        current_time = st_per_tier[tier]
                        if int(time_taken) < int(current_time):
                            print(time_taken+" > "+current_time)
                            st_per_tier[tier]      = time_taken
                            st_per_tier_name[tier] = name 
                    else:
                        st_per_tier[tier]      = time_taken
                        st_per_tier_name[tier] = name 
                else:
                    st_per_tier[tier]      = time_taken
                    st_per_tier_name[tier] = name
                ### SHORTEST TIME ###
                
                ### AVERAGE TIME ###
                if av_per_tier != {}:
                    if tier in av_per_tier:
                        curr_avg_time = av_per_tier[tier]
                        curr_avg_time = int(curr_avg_time) * (no_of_maps-1)
                        curr_avg_time = int(curr_avg_time) + int(time_taken)
                        curr_avg_time = int(curr_avg_time / no_of_maps)
                        av_per_tier[tier] = curr_avg_time
                    else:
                        av_per_tier[tier] = time_taken

                else:
                    av_per_tier[tier] = time_taken
                ### AVERAGE TIME ###
                ### MAPS ###

        if print_tiers == "y":         
            print("")
            print("### Breakdown by tiers ###")
            print("---------------------------------------------------------------------------------------------------------------------------------------------------")     
            for tier_order in tiers:
                if str(tier_order) in lt_per_tier.keys():
                    
                    print("Tier    Number of maps completed    Longest Map Time    Shortest Map Time    Average Map Time    Most XP Gained    Least XP Gained    AVG XP Gained")

                    print_string = str(tier_order)
                    print_string = print_string.ljust(8," ")
                    print_string = print_string + str(maps_per_tier[str(tier_order)])
                    print_string = print_string.ljust(36," ")
                    print_string = print_string + str(lt_per_tier[str(tier_order)])
                    print_string = print_string.ljust(56," ")
                    print_string = print_string + str(st_per_tier[str(tier_order)])
                    print_string = print_string.ljust(77," ")
                    print_string = print_string + str(av_per_tier[str(tier_order)])
                    print_string = print_string.ljust(97," ")
                    print_string = print_string + str(m_xp_per_tier[str(tier_order)])
                    print_string = print_string.ljust(115," ")
                    print_string = print_string + str(l_xp_per_tier[str(tier_order)])
                    print_string = print_string.ljust(134," ")
                    print_string = print_string + str(a_xp_per_tier[str(tier_order)]) 

                    
                    print(print_string)
                    print("")
            print("---------------------------------------------------------------------------------------------------------------------------------------------------")     

    else:
        input("No file found at %s. Hit enter to quit." % file_dir)
except:
    print("error")

finally:
    if xp_file:
        xp_file.close()
        print("\nQuiting!")
        input("Please enter to quit.")

########## MAIN BLOCK ##########

"""
my_value = input("enter dem value:")

for key, value in lvls_dict.items():
    if int(my_value) >=  value:
        current_lvl = key
    
    if int(my_value) < value:
        break


print("Your current level is: %s" % current_lvl)
time.sleep(100)
"""