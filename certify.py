from urllib.request import ssl, socket
import datetime, smtplib
import sqlite3
import platform
import os
import time
import sys
import re
from prettytable import PrettyTable

class ConsoleColor:
    # Color
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[97m'
    # Style
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # BackgroundColor
    BgBLACK = '\033[40m'
    BgRED = '\033[41m'
    BgGREEN = '\033[42m'
    BgORANGE = '\033[43m'
    BgBLUE = '\033[44m'
    BgPURPLE = '\033[45m'
    BgCYAN = '\033[46m'
    BgGRAY = '\033[47m'
    # End
    END = '\033[0m'


printit = False

if platform.system() == 'Windows':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


if os.path.exists("certify.db"):
    con = sqlite3.connect('certify.db')
    cursor = con.cursor()
else:
    clear()
    print("no database named 'certify.db. should i create a new one?")
    create_new_database = input("y/n: ")
    if create_new_database == "y":
        con = sqlite3.connect('certify.db')
        cursor = con.cursor()
        clear()
        print("new database named 'certify.db' was created right now.")
        time.sleep(2)
    else:
        exit()

clear()
try:
    with con:
        con.execute("""
            CREATE TABLE certify (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                port TEXT,
                notbefore TEXT,
                notafter TEXT, 
                ping TEXT
            );
        """)
    print("new table named 'certify' was created right now.")
except:
    print("welcomme back")
    time.sleep(1)


def printLogo():
    print("""
 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝ 
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝  
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║   
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝   
    by elias
    """)


def printMenu():
    clear()
    printLogo()
    print("""


Usage: python certify.py [OPTION] ...

    -d, --delete            Delete a domain from the db
            --all           Clear the table or delete the db
    -a, --add               Add a domain to the db
    -l, --list              List domains in db
            --all           To print more details
    -u, --update            Update expiry date
    -c, --create            Create pdf
    -s, --server            Start server-mode on localhost

Example:
    python certify.py -c pdf
    python certify.py --delete google.com 443
    python certify.py --list
    """)

def updatefunc():
    i = 1
    clear()
    printLogo()
    print("\n\nUpdate-Mode:\n")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM certify")
    domain_list = cursor.fetchall()
    for x in domain_list:
        hostname = x[1]
        port = x[2]
        print(str(i) + "/" + str(len(domain_list)) + ": " + hostname + ":" + port)
        i += 1
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname = hostname) as ssock:
                    certificate = ssock.getpeercert()
            x_notAfter = datetime.datetime.strptime(certificate['notAfter'], '%b  %d %H:%M:%S %Y %Z')
            x_notBefore = datetime.datetime.strptime(certificate['notAfter'], '%b  %d %H:%M:%S %Y %Z')
            x_notAfter_unix = time.mktime(x_notAfter.timetuple())
            x_notBefore_unix = time.mktime(x_notBefore.timetuple())
            cursor = con.cursor()
            cursor.execute('UPDATE certify SET notbefore="'+ str(x_notBefore_unix) +'", notafter="'+ str(x_notAfter_unix) +'" WHERE domain="'+ hostname +'"')
            con.commit()
            print("├─ ok")
        except:
            cursor = con.cursor()
            cursor.execute('UPDATE certify SET notbefore="error", notafter="error" WHERE domain="'+ hostname +'"')
            con.commit()
            print("├─ error")

def addfunc():
    clear()
    try:
        sys.argv[2]
        sys.argv[3]
        try:
            domain = re.match('(?=^.{,253}$)(?!^.+\.\d+$)(?=^[^-.].+[^-.]$)(?!^.+(\.-|-\.).+$)(?:[a-z\d-]{1,63}(\.|$)){2,127}', sys.argv[2], re.X | re.I)
            port = str(sys.argv[3])
            if domain and int(port) in range(1, 100000):
                domain = domain.group()
                try:
                    cursor = con.cursor()
                    cursor.execute('SELECT * FROM certify where domain="' + domain + '" and port="' + port + '"')
                    amout = len(cursor.fetchall())
                    if amout == 0:
                        try:
                            cursor = con.cursor()
                            cursor.execute('INSERT INTO certify(domain, port, notbefore, notafter, ping) VALUES("'+ domain +'", "'+ port +'", "n/a", "n/a", "n/a");')
                            con.commit()
                            print("domain valid and added to the db.")
                        except:
                            print("domain valid but error with adding to db")
                    else:
                        print(domain + ":" + port + " already in db")
                except:
                    print("failed to check if entry already present")
            else:
                print("domain not valid. please enter it like: google.ch")
        except:
            print("wrong domain format")
    except:
        print("wrong argument format. e.x: python certify.py -a <domain> <port>")

def deletefunc():
    clear()
    if sys.argv[2] == "--all":
        yescont1 = input("Are you sure you want to delete all data from the database? y/n: ")
        if yescont1 == "y":
            cursor = con.cursor()
            cursor.execute('DELETE FROM certify')
            con.commit()
            yescont2 = input("do you want to delete the database file as well? y/n: ")
            if yescont2 == "y":
                os.remove("certify.db")
    else:
        try:
            sys.argv[2]
            sys.argv[3]
            try:
                domain = re.match('(?=^.{,253}$)(?!^.+\.\d+$)(?=^[^-.].+[^-.]$)(?!^.+(\.-|-\.).+$)(?:[a-z\d-]{1,63}(\.|$)){2,127}', sys.argv[2], re.X | re.I)
                port = str(sys.argv[3])
                if domain and int(port) in range(1, 100000):
                    domain = domain.group()
                    try:
                        cursor = con.cursor()
                        cursor.execute('SELECT * FROM certify where domain="' + domain + '" and port="' + port + '"')
                        amout = len(cursor.fetchall())
                        if amout != 0:
                            cursor = con.cursor()
                            cursor.execute('DELETE FROM certify WHERE domain="'+ domain +'" and port="'+ port +'";')
                            con.commit()
                            print(""+domain+":"+port+" is removed now")
                        else:
                            print("no entry with " + domain + ":" + port + " found")
                    except:
                        print("domain valid but error with adding to db")
                else:
                    print("domain not valid. please enter it like: google.ch")
            except:
                print("wrong domain format")
        except:
            print("wrong argument format. e.x: python certify.py -d <domain> <port>")

def listfunc():
    clear()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM certify")
    domain_list = cursor.fetchall()
    table = PrettyTable()

    def printSimple():
        table.field_names = ["Domain:Port", "Days left"]
        table.align = "l"
        for x in domain_list:
            x_domain = str(x[1])
            x_port = str(x[2])
            x_notafter = str(x[4])
            if x_notafter == "error":
                x_daysleft = "error"
            elif x_notafter == "n/a":
                x_daysleft = "please update the db"
            else:
                x_daysleft = (datetime.datetime.fromtimestamp(float(x_notafter)) - datetime.datetime.today()).days
                if x_daysleft < 50:
                    x_daysleft = ConsoleColor.RED + str(x_daysleft) + ConsoleColor.END
            table.add_row([x_domain + ":" + x_port, x_daysleft])
        printLogo()
        if printit == True:
            print(table)

    def printAdvanced():
        table.field_names = ["Domain", "Port", "Not-Before (unix-timestamp)", "Not-After (unix-timestamp)", "Ping"]
        table.align = "l"
        for x in domain_list:
            x_domain = str(x[1])
            x_port = str(x[2])
            x_notbefore = str(x[3])
            x_notafter = str(x[4])
            x_ping = str(x[5])
            table.add_row([x_domain, x_port, x_notbefore, x_notafter, x_ping])
        printLogo()
        print(table)
    if len(sys.argv) > 2:
        if sys.argv[2] == "--all":
            printAdvanced()
        else:
            print("wrong format")
    else:
        printSimple()

def serverfunc():
    continue2 = True
    while continue2 == True:
        updatefunc()
        print("just updated. next update in 30min")
        time.sleep(1800)













try:
    sys.argv[1]
except:
    printMenu()
    exit()

if sys.argv[1] == "--update" or sys.argv[1] == "-u":
    updatefunc()
elif sys.argv[1] == "--add" or sys.argv[1] == "-a":
    addfunc()
elif sys.argv[1] == "--delete" or sys.argv[1] == "-d":
    deletefunc()
elif sys.argv[1] == "--list" or sys.argv[1] == "-l":
    printit = True
    listfunc()
elif sys.argv[1] == "--server" or sys.argv[1] == "-s":
    serverfunc()
elif sys.argv[1] == "--create" or sys.argv[1] == "-c":
    serverfunc()
elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    printMenu()
    exit()
else:
    clear()
    print("Wrong argument. Type '-h' or '--help'.")
    exit()



