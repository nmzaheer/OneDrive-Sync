# OneDrive-Sync
*Script for syncing files to OneDrive*

This program can be used to upload files from your folder to your OneDrive account

* To use this program, you will need to authorize the program by giving it permission to access and modify your OneDrive
* Click on the following URL [here](https://login.live.com/oauth20_authorize.srf?response_type=code&client_id=0000000044135BBF&scope=wl.basic+wl.skydrive_update+wl.offline_access&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf). 
* It will ask you to login and then you will be redirected to a page where you will have to give permission to the application
* You will be redirected to an empty page whose URL will be similar to the one below

``` 
https://login.live.com/oauth20_desktop.srf?code=ad3570b8-74be-238d-ef4d-f3e5fb4cdd03&lc=1033 
```

* Copy the code i.e. `ad3570b8-74be-238d-ef4d-f3e5fb4cdd03` to your clipboard.
* Run the program in your console and paste your authorization code
```
python main.py --authorize ad3570b8-74be-238d-ef4d-f3e5fb4cdd03
```
* Once authorization is successful, you can upload all files in your source folder to your OneDrive 
```
python main.py [source folder] [destination folder name in your OneDrive]
```

##Bugs
In case of bugs, please raise an issue in the issue tracker and I will attend to it.
