from datetime import date
from datetime import datetime
import linecache

def lay_egg(n):
    # datetime object containing current date and time
    today = datetime.now()    
    # dd/mm/YY H:M:S
    dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    name = n
    age = 0
    level = 0
    alive = True
    happy = 5
    hungry = 5
    dirty = 5
    f = open('tamapy_db.txt', 'w')
    f.write('NAME ' + name + '\n')
    f.write('AGE ' + str(age) + '\n')
    f.write('LEVEL ' + str(level) + '\n')
    f.write('ALIVE ' + str(alive) + '\n')
    f.write('HAPPY ' + str(happy) + '\n')
    f.write('HUNGRY ' + str(hungry) + '\n')
    f.write('DIRTY ' + str(dirty) + '\n')
    f.write('START ' + dt_string + '\n')
    f.closed

def print_squares(n,stat_name):
    match n:
        case 0:
            if stat_name=="happy":
                print("HAPPY □□□□□")
            if stat_name=="hungry":
                print("FULL  □□□□□")
            if stat_name=="dirt":
                print("CLEAN □□□□□")           
        case 1:
            if stat_name=="happy":
                print("HAPPY ■□□□□")
            if stat_name=="hungry":
                print("FULL  ■□□□□")
            if stat_name=="dirt":
                print("CLEAN ■□□□□")       
        case 2:
            if stat_name=="happy":
                print("HAPPY ■■□□□")
            if stat_name=="hungry":
                print("FULL  ■■□□□")
            if stat_name=="dirt":
                print("CLEAN ■■□□□")
        case 3:
            if stat_name=="happy":
                print("HAPPY ■■■□□")
            if stat_name=="hungry":
                print("FULL  ■■■□□")
            if stat_name=="dirt":
                print("CLEAN ■■■□□")  
        case 4:
            if stat_name=="happy":
                print("HAPPY ■■■■□")
            if stat_name=="hungry":
                print("FULL  ■■■■□")  
            if stat_name=="dirt":
                print("CLEAN ■■■■□")  
        case 5:
            if stat_name=="happy":
                print("HAPPY ■■■■■")
            if stat_name=="hungry":
                print("FULL  ■■■■■")
            if stat_name=="dirt":
                print("CLEAN ■■■■■")

def get_stats():
    f = open('tamapy_db.txt', 'r')
    for line in f:
        if line[2]=='P': #HAPPY
            happy=int(line[6])
            print_squares(happy,"happy")
        elif line[2]=='N': #HUNGRY
            hungry=int(line[7])
            print_squares(hungry,"hungry")
        elif line[2]=='R': #DIRTY
            dirt=int(line[6])
            print_squares(dirt,"dirt")
        elif line[2]=='M': #NAME
            print(line)
    f.close()

def play():
    print("Playing")

def feed():
    print("Feeding")
    f = open('./tamapy_db.txt', 'r+')
    f.seek(5)
    print(f)
    f.close()

    '''
    for line in f:
        if line[2]=='N': #HUNGRY
            value=int(line[7])
            new_value=value+1
            f.write('HUNGRY ' + str(new_value) + '\n')
    '''        
            

def clean():
    print("Cleaning")

    

def main():
#    lay_egg("Pau")
    get_stats()
#    feed()
#    get_stats()
    #f = open('./tamapy_db.txt', 'r+')
    line = linecache.getline('tamapy_db.txt', 5)
    print(line)
    linecache.clearcache()



if __name__ == "__main__":
    main()
