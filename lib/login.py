#!/usr/bin/python3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable warnings by default
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LOGIN_URL = "https://intranet.upv.es:443/pls/soalu/est_aute.intraalucomp"
LOGIN_DATA = {"id": "c", "estilo": "500", "vista": '', "param": '', "cua": "miupv", "dni": None, "clau": None}

session = requests.session()

def login(user, pswd):
    LOGIN_DATA["dni"] = user
    LOGIN_DATA["clau"] = pswd
    return session.post(LOGIN_URL, data=LOGIN_DATA, allow_redirects=True, verify=False, cookies=session.cookies)

