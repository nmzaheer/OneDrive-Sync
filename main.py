import argparse
import json
import os
import requests
import sys
'''
Go to the following URL and give consent to the app

https://login.live.com/oauth20_authorize.srf?response_type=code&client_id=0000000044135BBF&scope=wl.basic+wl.skydrive_update+wl.offline_access&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf

Copy the authentication code and paste it in the console
Example:
After you give consent, you will be redirected to the following URL

https://login.live.com/oauth20_desktop.srf?code=ad3570b8-74be-238d-ef4d-f3e5fb4cdd03&lc=1033


Copy the code i.e. ad3570b8-74be-238d-ef4d-f3e5fb4cdd03 and paste it in the console as follows

python main.py --authorize ad3570b8-74be-238d-ef4d-f3e5fb4cdd03
'''

CLIENT_ID = u'0000000044135BBF'
CLIENT_SECRET = u'WLNGheUBZYHjpJhratN1STpcyMSRPZ1d'
REDIRECT_URI = u'https://login.live.com/oauth20_desktop.srf'
OAUTH_URI = u'https://login.live.com/oauth20_token.srf'
AUTH_CODE = u''
API_URI = u'https://apis.live.net/v5.0/'
client = requests.Session()
TOKEN = {}
REFRESH_TOKEN = ''

def upload(folderpath, files, dest):
    for obj in files:
        filepath = folderpath + '/' + obj
        with open(filepath, 'rb') as f:
            response = client.put(API_URI + dest +'/files/'+obj, params=TOKEN, data=f)
            r = json.loads(response.content.decode('utf-8'))
        if 'error' in r.keys():
            print('Could not upload '+ r['name'])
        else:
            print(r['name'] + ' uploaded..')

def authorize(code):
    token_load = {u'client_id':CLIENT_ID,u'client_secret':CLIENT_SECRET,u'code':code,u'redirect_uri':REDIRECT_URI,u'grant_type':u'authorization_code'}
    response = client.post(OAUTH_URI, data=token_load, verify=True)
    r = json.loads(response.content.decode('utf-8'))
    if 'error' in r.keys():
        print(r['error_description'])
        sys.exit(0)
    else:
        refresh_token = r['refresh_token']
        with open('.token','w') as f:
            f.write(refresh_token)
        print("Authorization successful...")

def authenticate():
    global TOKEN
    global REFRESH_TOKEN
    with open('.token', 'r') as f:
        REFRESH_TOKEN = f.read()
    token_load = {u'client_id':CLIENT_ID,u'client_secret':CLIENT_SECRET,u'refresh_token':REFRESH_TOKEN,u'redirect_uri':REDIRECT_URI,u'grant_type':u'refresh_token'}
    response = client.post(OAUTH_URI, data=token_load, verify=True)
    r = json.loads(response.content.decode('utf-8'))
    if 'error' in r.keys():
        print(r['error_description'])
    access_token = r['access_token']
    TOKEN = {u'access_token':access_token}
    refresh_token = r['refresh_token']
    with open('.token','w') as f:
        f.write(refresh_token)
    return True

def main():
    parser = argparse.ArgumentParser(description='To upload files to OneDrive')
    parser.add_argument('--authorize', dest="auth",
                        help="Authorize this app by pasting the authorization code")
    parser.add_argument('src', nargs='?', help='Folder location where the file exists')
    parser.add_argument('dest', nargs='?', help='Folder name of the upload location in OneDrive')
    args = parser.parse_args()
    if args.auth:
        authorize(args.auth)
        sys.exit(0)
    local_path = os.path.expanduser(args.src)
    if(not authenticate()):
        print("Authentication failed....")
        sys.exit(0)
    response = client.get(API_URI+u'me/skydrive/files', params=TOKEN)
    r = json.loads(response.content.decode('utf-8'))
    folderlist = {elem['name']:elem['id'] for elem in r['data']}
    if args.dest not in folderlist.keys():
        print("Folder does not exists....")
        sys.exit(0)
    response = client.get(API_URI+folderlist[args.dest]+u'/files', params=TOKEN)
    r = json.loads(response.content.decode('utf-8'))
    filelist = [elem['name'] for elem in r['data']]
    newfile = []
    for filename in os.listdir(local_path):
        if filename not in filelist:
            newfile.append(filename)
    if newfile:
        print("The following files are not listed in the OneDrive folder")
        for elem in newfile:
            print(elem)
        option = input("Do you want to upload them?(y/n):")
        if option  == 'y':
            upload(local_path, newfile, folderlist[args.dest])
        else:
            print("OK !!")
    else:
        print("All files in the folder are up to date")            
                
if __name__ == '__main__':
    main()
                
