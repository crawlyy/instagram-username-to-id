"""
Reads data from usernames.txt
checks each username for the user ID
"""
import time
import requests
import json
import sys
from bs4 import BeautifulSoup


def getPK(html):
    try:
        pk = html.split("profilePage_").pop()
        pk = pk.split('"')[0]
        if '<!DOCTYPE html>' in pk:
            return False
        return pk
    except Exception,e:
        print e
    return False

fout = open('keys.json','w')
data = [x.strip() for x in open('username.txt','r').readlines()]
burnt = []

dict = {}
county = 0
####

for user in data:
    sys.stdout.flush()
    if not user in burnt:
        try:
            r = requests.get('https://www.instagram.com/' + user)
            ret = getPK(r.text)
            if ret:
                print county, ' ', user, ' | ', ret
                burnt.append(user)
                dict[user] = ret
                county+=1
            else:
                sys.stdout.flush()
                print 'retrying...'
                for x in range(1,10):
                    print 30*x
                    sys.stdout.flush()
                    time.sleep(30*x)
                    r = requests.get('https://www.instagram.com/' + user)
                    ret = getPK(r.text)
                    if ret:
                        print county, ' ', user, ' | ', ret
                        burnt.append(user)
                        dict[user] = ret
                        county+=1
                        break
        except Exception,e:
            print e
            time.sleep(60)

####
try:
    json.dumps(dict,fout)
except:
    try:
        json.dump(dict,fout)
    except:
        pass

