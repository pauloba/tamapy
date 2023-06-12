from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime
#import linecache
#import fileinput
import os
import time



'''
FUNCTION lay_egg(pet_name str)
------------------------------
- Initializes name, age, alive, healthy, happy, full, clean, poo.
- Values are stored in a text file for persitence.
- POO is a hidden value ranges from 0-6.
- From main() when POO=6 the poop() function is called.
'''
def lay_egg(pet_name):
    # datetime object containing current date and time
    today = datetime.now()    
    # dd/mm/YY H:M:S
    date_time = today.strftime("%d/%m/%Y %H:%M:%S")
    f = open("tamapy_db.txt", "w")
    f.write("0 NAME " + pet_name + "\n")
    f.write("1 AGE " + "0" + "\n")
    f.write("2 ALIVE " + "T" + "\n")
    f.write("3 HEALTH " + "5" + "\n")
    f.write("4 HAPPY " + "5" + "\n")
    f.write("5 FULL " + "5" + "\n")
    f.write("6 CLEAN " + "5" + "\n")
    f.write("7 POO " + "0" + "\n")
    f.write("8 START " + date_time + "\n")
    f.write("9 LIGHT " + "T" + "\n")
    f.close()

'''
FUNCTION print_squares(stat_value int, stat_name str)
----------------
- Prints the values with empty or full squares for stats
- Stats always shown: HAPPY, FULL, CLEAN.
- HEALTHY only shown when <=3.
'''
def print_squares(stat_value,stat_name):
    match stat_name:
        case 0:
            if stat_name=="happy":
                print("🔴 HAPPY   □□□□□")
            if stat_name=="full":
                print("🔴 FULL    □□□□□")
            if stat_name=="clean":
                print("🔴 CLEAN   □□□□□")
            if stat_name=="health":
                print("🔴 HEALTHY □□□□□")          
        case 1:
            if stat_name=="happy":
                print("🔴 HAPPY   ■□□□□")
            if stat_name=="full":
                print("🔴 FULL    ■□□□□")
            if stat_name=="clean":
                print("🔴 CLEAN   ■□□□□")   
            if stat_name=="health":
                print("🔴 HEALTHY ■□□□□")
        case 2:
            if stat_name=="happy":
                print("🔴 HAPPY   ■■□□□")
            if stat_name=="full":
                print("🔴 FULL    ■■□□□")
            if stat_name=="clean":
                print("🔴 CLEAN   ■■□□□")
            if stat_name=="health":
                print("🔴 HEALTHY ■■□□□")
        case 3:
            if stat_name=="happy":
                print("🟠 HAPPY   ■■■□□")
            if stat_name=="full":
                print("🟠 FULL    ■■■□□")
            if stat_name=="clean":
                print("🟠 CLEAN   ■■■□□")
            if stat_name=="health":
                print("🟠 HEALTHY ■■■□□")                 
        case 4:
            if stat_name=="happy":
                print("🟠 HAPPY   ■■■■□")
            if stat_name=="full":
                print("🟠 FULL    ■■■■□")  
            if stat_name=="clean":
                print("🟠 CLEAN   ■■■■□")
#            if stat_name=="health":
#                print("🟠 HEALTHY ■■■■□")
        case 5:
            if stat_name=="happy":
                print("🟢 HAPPY   ■■■■■")
            if stat_name=="full":
                print("🟢 FULL    ■■■■■")
            if stat_name=="clean":
                print("🟢 CLEAN   ■■■■■")
#            if stat_name=="health":
#                print("🟢 HEALTHY ■■■■■")

'''
FUNCTION get_stats()
------------------------------
Reads from tamapy_db.txt:
- Prints stats for HAPPY, FULL, CLEAN.
  HEALTH is shown only if it reaches values<=3
'''
def get_stats():
    file = open("tamapy_db.txt", "r")
    for line in file:
        if line[0]=="0": #NAME
            print(line[2:]) # Remove 2 first characters that are the line number
        elif line[0]=="3":
            if int(line[9])<=3: #To surprise player SHOW ONLY IF HEALTH<=3
                healthyness=int(line[9])
                print_squares(healthyness,"health")
        elif line[0]=="4": #HAPPY
            happyness=int(line[8])
            print_squares(happyness,"happy")
        elif line[0]=="5": #FULL
            fullness=int(line[7])
            print_squares(fullness,"full")
        elif line[0]=="6": #CLEAN
            cleanness=int(line[8])
            print_squares(cleanness,"clean")
    file.close()


def play():
    print("Playing")

'''
FUNCTION feed()
------------------------------
Writes to tamapy_db.txt:
- Increases FULL by 1.
- Increases POO by 2. Values range [0-6]
'''
def feed():
    print("Feeding")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="5": #FULL status
            fullness_old = int( line[7] )
            if 0 <= fullness_old < 5: # Feed only if value between 0 and 4
                fullness_new = (fullness_old+1) if fullness_old <5 else 5
                old_str = "5 FULL " + str(fullness_old)
                new_str = "5 FULL " + str(fullness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif fullness_old == 5: # If fullness already at MAX do not feed
                file_out.write(line)
        if line[0]=="7": #POO status
            poo_old = int( line[6] )
            if poo_old <6: # Increase only if the value is less than MAX (MAX=6)
                poo_new = (poo_old+1) if poo_old <6 else 6
                old_str = "7 POO " + str(poo_old)
                new_str = "7 POO " + str(poo_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif poo_old == 6: # If poo already at MAX do not increase
                file_out.write(line)
        elif line[0]!="5":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")


'''
FUNCTION poop()
------------------------------
Writes to tamapy_db.txt:
- Decreases CLEAN by 1.
- Decreases FULL by 1.
'''
def poop():
    print("Pooping")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        # DECREASE FULLNESS BY 1 WHEN POOPING
        if line[0]=="5": #FULL STATUS
            fullness_old = int( line[7] )
            if 0 <= fullness_old <= 5: # Poop only if value between 1 and 5
                fullness_new = (fullness_old-1) if fullness_old >0 else 0
                old_str = "5 FULL " + str(fullness_old)
                new_str = "5 FULL " + str(fullness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif fullness_old == 0: # If fullness at MIN do not decrease FULL
                file_out.write(line)
        # DECREEASE CLEANNESS BY 1 WHEN POOPING
        if line[0]=="6": #CLEAN STATUS
            cleanness_old = int( line[8] )
            if 0 <= cleanness_old <=5: # Dirt only if value between 1-5
                cleanness_new = (cleanness_old-1) if cleanness_old > 0 else 0
                old_str = "6 CLEAN " + str(cleanness_old)
                new_str = "6 CLEAN " + str(cleanness_new)
                file_out.write( line.replace(old_str, new_str) ) 
        elif line[0]!="5" and line[0]!="6":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

'''
FUNCTION clean()
------------------------------
Writes to tamapy_db.txt
- Increases CLEAN by 1.
'''
def clean():
    print("Cleaning")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        # INCREASE CLEANNESS BY 1
        if line[0]=="6": #CLEAN STATUS
            cleanness_old = int( line[8] )
            if 0 <= cleanness_old < 5: # Clean only if value between 0 and 4
                cleanness_new = (cleanness_old+1) if cleanness_old <5 else 5
                old_str = "6 CLEAN " + str(cleanness_old)
                new_str = "6 CLEAN " + str(cleanness_new)
                file_out.write( line.replace(old_str, new_str) )    
            if cleanness_old == 5: # If cleanness at MAX do not clean
                file_out.write(line) 
        elif line[0]!="6":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

'''
FUNCTION get_sick()
------------------------------
- Decreases HEALTH by 1.
'''
def get_sick():
    print("Getting sick")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="3": #HEALTH STATUS
            healthyness_old = int( line[9] )
            if 0 <= healthyness_old <= 5: # Get sick only if value between 0 and 4
                healthyness_new = (healthyness_old-1) if healthyness_old>0 else 0
                old_str = "3 HEALTH " + str(healthyness_old)
                new_str = "3 HEALTH " + str(healthyness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif healthyness_old == 0: # If health already at MIN don't decrease
                file_out.write(line)           
        elif line[0]!="3":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

'''
FUNCTION take_medicine()
------------------------------
- Increases HEALTH by 1.
'''
def take_medicine():
    print("Taking medicine")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="3": #HEALTH STATUS
            healthyness_old = int( line[9] )
            if 0 <= healthyness_old <= 5: # Cure only if value between 0 and 4
                healthyness_new = (healthyness_old+1) if healthyness_old>4 else 5
                old_str = "3 HEALTH " + str(healthyness_old)
                new_str = "3 HEALTH " + str(healthyness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif healthyness_old == 5: # If health already at MAX don't increase
                file_out.write(line)           
        elif line[0]!="3":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

'''
FUNCTION calculate_age()
-------------------------
Writes do tamapy_db.txt
updates the AGE.
Tamapy age correlates to human age.
'''
def calculate_age():
    print("Calculating age")
    
    file_in = open("tamapy_db.txt", "r")
    #file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="8": #Tamapy birth date
            birth_line = line   
    file_in.close()
    birth_date = birth_line.split(',')
    print("birth_line    " + birth_line + "\n")
    #print("birth_date    " + birth_date + "\n")
    print("birth_date[0]    " + birth_date[0] + "\n")
 #   print("birth_date[1]    " + birth_date[1] + "\n")
 #   print("birth_date[2]    " + birth_date[2] + "\n")
#    print("birth_date[3]    " + birth_date[3] + "\n")

    today = date.today()
    age = relativedelta(today, birth_date[2])
    return age.years
    # Test the function
    birth_date = date(1997, 2, 3)
    age = calculate_age(birth_date)
    print(f"Age in years: {age}")    

'''
FUNCTION sleep()
-------------------------
Writes do tamapy_db.txt:
- Shows message that the character is sleeping.
- Switches light on "after" sleeping.
- If light OFF increases health by 1.
- If light ON decreases health by 1.
'''
def sleep():
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="0": # Line with the NAME
            print(line[6:] + "Is sleeping ...")
            time.sleep(5)    
            print("  Zzz... zzz... zzz...")
            time.sleep(5)
            print("  Zzz... zzz... zzz...")
        if line[0]=="9": # Line with the LIGHT STATUS
            light_status = line[8]
            light_on = "T"
            old_str = "9 LIGHT " + str(light_status)
            new_str = "9 LIGHT " + str(light_on)
            file_out.write( line.replace(old_str, new_str) )    
        elif line[0]=="3" and light_status=="T": # Get sick only if light ON
            healthyness_old = int(line[9])
            healthyness_new = (healthyness_old-1) if healthyness_old>0 else 0
            old_str = "3 HEALTH " + str(healthyness_old)
            new_str = "3 HEALTH " + str(healthyness_new)
            file_out.write( line.replace(old_str, new_str) )     
            if healthyness_old == 0: # If health already at MIN don't decrease
                file_out.write(line)           
        elif line[0]!="3":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")


'''
FUNCTION light_off()
-------------------------
Writes do tamapy_db.txt:
- Updates LIGTH to "T" (true).
'''
def light_off():
    print("Switching light off")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="9": #Light STATUS
            light_old = line[8]
            if light_old=="F": # Switch off only if LIGHT==T; T means true
                light_new = "T"
                old_str = "6 CLEAN " + str(light_old)
                new_str = "6 CLEAN " + str(light_new)
                file_out.write( line.replace(old_str, new_str) )    
            if light_old =="T": # If light already ON do not switch ON
                file_out.write(line) 
        elif line[0]!="6":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")


'''

- When POO==6 poo() function is called.

'''

'''
TO DO 
- clear screen
- menu for actions
- generic home directory path
- fix calculate age()
- fix sleep()
- create test suite
'''

def main():


#    linecache.clearcache()
#    lay_egg("★☆. · · ·.☆★BiZC0CHiT0oo0★☆. · · ·.☆★")
# Clearing the Screen
#   os.system('cls')

    sleep()

#    calculate_age()

# TEST GET_SICK
    '''
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    get_stats()
    get_sick()
    ''' 
# TEST CLEAN
    '''
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    clean()
    get_stats()
    '''

# TEST POOP
    '''
    get_stats()
    feed()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    poop()
    get_stats()
    '''

if __name__ == "__main__":
    main()
