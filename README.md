## YOUTUBE VIDEO TO MP3 PROJECT

![](https://github.com/Shubhammalik/youtube-to-mp3/blob/main/img/youtube-to-mp3.jpg)
&nbsp;

&nbsp;

&nbsp;

*************************  INSTALLATION AND RUNNING  *************************

1) Download the project and run the below requirements in the project folder terminal
	pip install -r /path/to/requirements.txt

1) Sign up if not already a google member (gmail)

2) Go to https://console.cloud.google.com and create a new project under google console (name it youtube-project)

3) Create Authorization consent screen (under left panel on console OAuth Consent Screen)

4) Under credentials (on google console), go to create credentials (on top)

	i) Create Authorization ClientID (not used now but will be in future)
	
	ii) Download the json file and rename it as authorization.json
	
	iii) Create new API key

5) Create new json (api.json) for

	i) CHANNEL_ID (any youtube channel ID)
	
	ii) DEVELOPER_KEY (API Key created above)
	
	iii) YOUTUBE_API_SERVICE_NAME: 'youtube'
	
	iv) YOUTUBE_API_VERSION: 'v3'

6) Give access to youtube API v3 using the same gmail address
 https://console.cloud.google.com/apis/library/youtube.googleapis.com

7) In code directory create a config folder and place both the json files there

8) Run the code file main.py with variable download_new_data = 1 in main function and ENJOY!!

9) Optional: use "pip freeze > requirements.txt" command without quotes in project terminal to write a new requirement.txt file
&nbsp;

&nbsp;

&nbsp;

*********************************  WORKING  *********************************

TRY the youtubeAPI: https://developers.google.com/youtube/v3/code_samples/code_snippets


FILE: main.py
- Runs the code and does the job for you


FILE: generate_environment_variables.py
- Reads the json data from both the json files and writes the variables into new .env file
- Check for existing .env file otherwise create a new one and loads them for the project
- Tests the newly created environment variables


FILE: create_youtube_list.py
- Fetches all the playlist of ChannelID provided as environment variable
	URL used: https://www.youtube.com/channel/[YOUR_CHANNEL_ID]/playlists
- Hits the youtube API for each playlist to get a list of associated videos
- Writes the data to a json file for each playlist
- Checks and loads the json file for the application, create one if not already present


FILE: music_download.py
- This is where the FUN begins!
- Takes help of the site [https://ythub.cc] to get the downlodable mp3 file of each video
- Regex is used the get the file ID of the mp3 file
- The code interacts with site's API and fetches the dynamic link in real time for each mp3 file ID
- This code is robus enough to handle all the boundary cases of file download, a new json file will be created which will store the download history of all songs
- The code will fetch new video list every time you run it but will only download the new file added to the playlist/Channel
&nbsp;

&nbsp;

&nbsp;

**************************** OTHER USEFUL ITEMS  *****************************

1) Regex Identifier
u002F?file_id=

2) Download Site
https://ythub.cc

3) Download Site video download link
https://ythub.cc/download/[YOUTUBE_VIEDO_ID].html

4) Response from API (link)
https://api.ythub.cc/v1/youtube/get-download-link/?file_id=[FILE_ID_FROM_SITE]

5) Extracted download link
https://dl20.ythub.cc/v1/youtube/download/?file_id=[FILE_ID_FROM_SITE]


