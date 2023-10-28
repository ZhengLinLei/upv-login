#!/usr/bin/python3

# IMPORT LIBRARIES
import argparse
from lib.login import *

# Main check
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--min', help='Min. range', required=True)
    parser.add_argument('-M', '--max', help='Max. range', required=True)
    # Add verbose option
    parser.add_argument('-v', '--verbose', help='Verbose data', action='store_true')
    args = parser.parse_args()

    #!TODO: Avaliable only for DNI. NIE and PASSPORT not implemented
    user = args.min
    password = "xxxxxx"


    while user <= args.max:
        r0 = login(user, password)
        
        if "ERR55" not in r0.url:
            if args.verbose:
                print(user)
            # User exist
            open('./users.txt', 'a').write(user + '\n')

        user = str(int(user) + 1)

    print("========= End =========")


