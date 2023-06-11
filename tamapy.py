from datetime import date
from datetime import datetime
import linecache
import fileinput
import os

def lay_egg(n):
    # datetime object containing current date and time
    today = datetime.now()    
    # dd/mm/YY H:M:S
    date_time = today.strftime("%d/%m/%Y %H:%M:%S")
    name = n
    age = 0
    sick = 0
    alive = True
    happy = 5
    full = 5
    clean = 5
    f = open("tamapy_db.txt", "w")
    f.write("0 NAME " + name + "\n")
    f.write("1 AGE " + str(age) + "\n")
    f.write("2 SICK " + str(level) + "\n")
    f.write("3 ALIVE " + str(alive) + "\n")
    f.write("4 HAPPY " + str(happy) + "\n")
    f.write("5 FULL " + str(full) + "\n")
    f.write("6 CLEAN " + str(clean) + "\n")
    f.write("7 START " + date_time + "\n")
    f.write("8 NOW " + date_time + "\n")
    f.closed

def print_squares(n,stat_name):
    match n:
        case 0:
            if stat_name=="happy":
                print("HAPPY □□□□□")
            if stat_name=="full":
                print("FULL  □□□□□")
            if stat_name=="clean":
                print("CLEAN □□□□□")           
        case 1:
            if stat_name=="happy":
                print("HAPPY ■□□□□")
            if stat_name=="full":
                print("FULL  ■□□□□")
            if stat_name=="clean":
                print("CLEAN ■□□□□")   
            if stat_name=="sick":
                print("☠")
        case 2:
            if stat_name=="happy":
                print("HAPPY ■■□□□")
            if stat_name=="full":
                print("FULL  ■■□□□")
            if stat_name=="clean":
                print("CLEAN ■■□□□")
            if stat_name=="sick":
                print("☠☠")
        case 3:
            if stat_name=="happy":
                print("HAPPY ■■■□□")
            if stat_name=="full":
                print("FULL  ■■■□□")
            if stat_name=="clean":
                print("CLEAN ■■■□□")
            if stat_name=="sick":
                print("☠☠☠")                 
        case 4:
            if stat_name=="happy":
                print("HAPPY ■■■■□")
            if stat_name=="full":
                print("FULL  ■■■■□")  
            if stat_name=="clean":
                print("CLEAN ■■■■□")
            if stat_name=="sick":
                print("☠☠☠☠")  
        case 5:
            if stat_name=="happy":
                print("HAPPY ■■■■■")
            if stat_name=="full":
                print("FULL  ■■■■■")
            if stat_name=="clean":
                print("CLEAN ■■■■■")
            if stat_name=="sick":
                print("☠☠☠☠☠")

def get_stats():
    file = open("tamapy_db.txt", "r")
    for line in file:
        if line[0]=="0": #NAME
            print(line[2:]) # Remove 2 first characters that are the line number
        elif line[0]=="2" and line[7]>="0": #SICK
            sickness=int(line[7])
            print_squares(sickness,"sick")
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


def feed():
    print("Feeding")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="5": #FULL STATUS
            fullness_old = int( line[7] )
            if 0 <= fullness_old < 5: # Feed only if value between 0 and 4
                fullness_new = fullness_old+1
                old_str = "5 FULL " + str(fullness_old)
                new_str = "5 FULL " + str(fullness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif fullness_old == 5: # If fullness already at MAX do not feed
                file_out.write(line)           
        elif line[0]!="5":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

def poop():
    print("Pooping")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        # DECREASE FULLNESS BY 1 WHEN POOPING
        if line[0]=="5": #FULL STATUS
            fullness_old = int( line[7] )
            if 0 <= fullness_old <= 5: # Poop only if value between 1 and 5
                fullness_new = (fullness_old-1) if fullness_old > 0 else 0
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

def get_sick():
    print("Getting sick")
    file_in = open("tamapy_db.txt", "r")
    file_out = open("tamapy_db.tmp", "wt") 
    for line in file_in:
        if line[0]=="2": #SICK STATUS
            sickness_old = int( line[7] )
            if 0 <= sickness_old < 5: # Get sick only if value between 0 and 4
                sickness_new = sickness_old+1
                old_str = "5 FULL " + str(sickness_old)
                new_str = "5 FULL " + str(sickness_new)
                file_out.write( line.replace(old_str, new_str) )     
            elif sickness_old == 5: # If sickness already at MAX don't increase
                file_out.write(line)           
        elif line[0]!="2":
            file_out.write(line)
    file_in.close()
    file_out.close()
    os.remove("/home/pau/src/tamapy/tamapy_db.txt")
    os.rename("/home/pau/src/tamapy/tamapy_db.tmp","tamapy_db.txt")

def take_medicine():
    print("Taking medicine")

def main():
#    linecache.clearcache()
#    lay_egg("★☆. · · ·.☆★BiZC0CHiT0oo0★☆. · · ·.☆★")


# TEST GET_SICK
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
