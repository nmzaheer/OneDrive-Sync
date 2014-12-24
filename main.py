import os
import requests

'''
Go to the following URL and give consent to the app

https://login.live.com/oauth20_authorize.srf?response_type=code&client_id=0000000044135BBF&scope=wl.basic+wl.skydrive_update&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf

Copy the authentication code and paste it in the console

'''

CLIENT_ID = u'0000000044135BBF'
CLIENT_SECRET = u'WLNGheUBZYHjpJhratN1STpcyMSRPZ1d'
REDIRECT_URI = u'https://login.live.com/oauth20_desktop.srf'
AUTH_URI = u'https://login.live.com/oauth20_authorize.srf'
OAUTH_URI = u'https://login.live.com/oauth20_token.srf'
AUTH_CODE = u''
API_URI = u'https://apis.live.net/v5.0/'

def main():
    client = requests.Session()
    AUTH_CODE = input(u"Enter the code here : ")
    token_load = {u'client_id':CLIENT_ID,u'client_secret':CLIENT_SECRET,u'code':AUTH_CODE,u'redirect_uri':REDIRECT_URI,u'grant_type':u'authorization_code'}
    response = client.post(OAUTH_URI, data=token_load, verify=True)
    r = response.json()
    access_token = r['access_token']
    auth_token = r['authentication_token']
    token = {u'access_token':access_token}
    response = client.get(API_URI+u'me/skydrive/files', params=token)
    r = response.json()
    folder_dict = {elem['name']:elem['id'] for elem in r['data']}
    localfolder_path = os.path.expanduser('~/Downloads/Nuclear Energy/test')
    for filename in os.listdir(localfolder_path):
        filepath = localfolder_path + '/' + filename
        with open(filepath, 'rb') as f:
            response = client.put(API_URI+folder_dict['Nuclear Energy']+'/files/'+filename, params=token, data=f)
            r = response.json()
            print(r['name']+' uploaded')
    response = client.get(API_URI+folder_dict['Nuclear Energy']+'/files', params=token)
    r = response.json()
    print('\n\nThe following files are available in the Nuclear Energy')
    for elem in r['data']:
        print(elem['name'])

if __name__ == '__main__':
    main()
                
