"""

    Author: ZLL
    Disclaimer: Use it in your own risk

    How to use it?

    - Clone repository
    - Let path structure as it was cloned
    - Execute python script : python3 getimage.py --year $year --range 000:999 --output ../folder --user $user --password $password
    - All the result will be shown in result.txt
    - This action will take few minutes


    Explanation:

    Every student id is composed by 3 parts:

    YYYIIITT

    - year (YYY): Every faculty+year has their own ID First 3 digits of composition of the school year
    (That means that if you have entered university in 2020-2021 to ETSINF faculty, the id will be 698)
    TODO: Find the relation between ids, they are faculty that can have consecutive ids, 
    TODO: or maybe they are students from different faculty going to the same subject class

    - id (III): 3 digits of the student id, it is a consecutive number. That means that every faculty cannot have more than 999 students

    - type (TT): 99 means student
    TODO: Find the meaning of the other types



    You can get a mosaic after getting all by running the following command:
    sudo apt-get install imagemagick
    montage *.ico -tile x -geometry +2+2 mosaic.png

"""

import requests, shutil, sys, argparse, os
from common.mosaic import create_mosaic

s = requests.session()
user, passwd = "", ""
url = "https://intranet.upv.es/foto/get/%d.gif"
headers = {
    "Accept": "image/webp,image/avif,image/jxl,image/heic,image/heic-sequence,video/*;q=0.8,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://intranet.upv.es/pls/soalu/sic_al.lis?p_vista=intranet&p_idioma=c&p_caca=2024&P_asi=11553&P_ACTION=generarorla",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=5",
    "Author": "zll"
}

def getImage(id: str, output: str) -> bool: 
    try:
        response = s.get(url.replace("%d", id), headers=headers, stream=True)
        if response.status_code == 200:
            with open(f"{output}/{id}.gif", "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            del response
            return True
        else:
            return False
    except Exception as e:
        print(f"Excepción durante la solicitud GET: {e}")


def login(user: str, passwd: str) -> int:
    login_url = "https://intranet.upv.es:443/pls/soalu/est_aute.intraalucomp"
    login_data = {"id": "c", "estilo": "500", "vista": '', "param": '', "cua": "miupv", "dni": user, "clau": passwd}
    response = s.post(login_url, data=login_data)

    if "Persona no asociada como alumno en la UPV" in response.text:
        return (1, "User not found")

    if ("El PIN ha de ser un valor numérico" in response.text) or ("Clave de acceso no validada" in response.text):
        return (2, "Password incorrect")

    return (0, "")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', help='Every faculty+year has their own ID', required=True)
    parser.add_argument('-r', '--range', help='The range of student id', required=True)
    parser.add_argument('-o', '--output', help='Folder to save the output files', required=True)
    parser.add_argument('-u', '--user', help='Username to login', required=True)
    parser.add_argument('-p', '--password', help='Password to login', required=True)
    args = parser.parse_args()
    user = args.user
    passwd = args.password

    # Variables
    year, student_range, output = args.year, args.range, args.output

    iRet = login(user, passwd)
    if iRet[0] != 0:
        print(f"Error: Login failed. {iRet[1]}")
        sys.exit(iRet[0])


    # If output folder does not exist, create it
    if not os.path.exists(output):
        os.makedirs(output)

    for i in range(int(student_range.split(":")[0]), int(student_range.split(":")[1]) + 1):
        id = year + str(i).zfill(3) + "99"
        iRet = getImage(id, output)
        print(f"Image {id} saved in {output} ----------------- {i}/{int(student_range.split(':')[1])}    ------ {iRet}")

    create_mosaic(output, f"{output}/mosaic.png")