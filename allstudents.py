"""

    Author: ZLL
    Disclaimer: Use it in your own risk

    How to use it?

    - Clone repository
    - Let path structure as it was cloned
    - Execute python script : python3 allstudents.py --user $user --password $password --surname ./source/surname.txt -d > result.txt 2> error.log
    - All the result will be shown in result.txt
    - This action will take few minutes
    

    For no degree name label add -n
    python3 allstudents.py --user $user --password $password --surname ./source/surname.txt -d -n > result.txt 2> error.log

"""

import requests, argparse, json, sys, os, re

"""
Usage: python3 sys.argv[0] --user $user --password $password --surname $path_to_file
Usage: python3 sys.argv[0] -u $user -p $password -s $path_to_file

Help: python3 sys.argv[0] --help

Example: python3 allstudents.py --user $user --password $password --surname ./source/surname.txt -d > result.txt 2> error.log
"""

FACULTY_FILE="./source/facultades/directory.json"
DEGREE_FILE="./source/carreras/directory.json"

s = requests.session()


# Endpoint
url = "https://intranet.upv.es/pls/soalu/sic_dal.Buscar_Alumno?P_IDIOMA=c&P_VISTA=intranet"
pattern = r'<span style="font-style: italic;">(.*?)</span>.*?ParseEmail\(\'(.*?)\'\)'
user, passwd = "", ""

# Headers configuration
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate", 
    "Upgrade-Insecure-Requests": "1", 
    "Sec-Fetch-User": "?1", 
    "Te": "trailers", 
    "Author": "zll",
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "same-origin", 
}

# POST data
post_data = {
    "P_IDIOMA": "c",
    "P_VISTA": "intranet",
    "p_dni": "",
    "p_nom": "$FILL",
    "p_cen": "$FILL",
    "p_tit": "$FILL",
    "P_CODASI": "",
    "p_caca": "1",
    "p_verselect": "",
    "P_CABECERA": "1"
}




def error_selector(html: str, category: int) -> (int, str):

    if category == 0:
        # Login errors
        if "Persona no asociada como alumno en la UPV" in html:
            return (1, "User not found")

        if ("El PIN ha de ser un valor numérico" in html) or ("Clave de acceso no validada" in html):
            return (2, "Password incorrect")

        return (0, "")

    elif category == 1:

        if "Nombre muy corto" in html:
            return (2, "Apellido muy corto")

        if "Error" in html:
            iRet = login(user, passwd)
            if iRet[0] != 0:
                if not noerror: sys.stderr.write(f"Error Selector: {iRet[1]} \n")
                sys.exit(iRet[0])
            return (1, "Generic Error")
        


        return (0, "")

def parseListStudents(html: str) -> int:

    iRet = error_selector(html, 1)

    if iRet[0] != 0: 
        sys.stderr.write(f"Error Selector: {iRet[1]}\n")
        return iRet

    # Parse HTML table
    matches = re.findall(pattern, html, re.DOTALL)

    for match in matches:
        print(f"{match[0]}, {match[1].replace(' ', '')}", end="\n", flush=True)

    return iRet

def login(user: str, passwd: str) -> int:
    login_url = "https://intranet.upv.es:443/pls/soalu/est_aute.intraalucomp"
    login_data = {"id": "c", "estilo": "500", "vista": '', "param": '', "cua": "miupv", "dni": user, "clau": passwd}
    response = s.post(login_url, data=login_data)

    # Check login
    return error_selector(response.text, 0)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='Username to login', required=True)
    parser.add_argument('-p', '--password', help='Password to login', required=True)
    parser.add_argument('-s', '--surname', help='Surname List File Path', required=True)
    parser.add_argument('-d', '--debug', help='Activate debug mode. More logs', action='store_true')
    parser.add_argument('-nl', '--nolabel', help='Disable Faculty and Degree title', action='store_true')
    parser.add_argument('-ne', '--noerror', help='Disable error', action='store_true')
    args = parser.parse_args()
    user = args.user
    passwd = args.password

    # First letters of password
    surname_path = args.surname
    debug = args.debug
    nolabel = args.nolabel
    noerror = args.noerror

    print(f"Debug mode: {debug}", end="\n", flush=True)

    if not os.path.isfile(surname_path) or not os.path.isfile(FACULTY_FILE) or not os.path.isfile(DEGREE_FILE):
        sys.stderr.write("Archivos faltantes\n")
        sys.exit(1)

    # Files
    faculty, degree, surname = json.load(open(FACULTY_FILE, 'r')), json.load(open(DEGREE_FILE, 'r')), [line.strip() for line in open(surname_path).readlines()]

    iRet = login(user, passwd)
    if iRet[0] != 0:
        if not noerror: sys.stderr.write(f"Error Selector: {iRet[1]}\n")
        sys.exit(iRet[0])


    # for faculty
    for f in faculty:
        name, v = f['nombre'], f['value']
        if not nolabel: print(f"+ {name}", end="\n", flush=True)

        for d in degree[v]:
            nameD, vD = d['text'], d['value']
            if not nolabel: print(f"- {nameD}", end="\n", flush=True)

            for n in surname:
                if debug:
                    sys.stderr.write(f"Trying with {n} > {nameD} > {name} \n")

                post_data["p_nom"] = n
                post_data["p_cen"] = v
                post_data["p_tit"] = vD

                response = s.post(url, headers=headers, data=post_data)

                iRet = 1

                # Verify
                if response.status_code == 200:
                    iRet = parseListStudents(response.text)
                else:
                    if not noerror: sys.stderr.write(f"Error conn: {response.status_code} for : {n} > {nameD} > {name} \n")

                    # Retry
                    response = s.post(url, headers=headers, data=post_data)

                    if response.status_code == 200:
                        iRet = parseListStudents(response.text)
                    else:
                        if not noerror: sys.stderr.write(f"Error conn: {response.status_code} for : {n} > {nameD} > {name} (Omitted) \n")

                sys.stderr.flush()




    