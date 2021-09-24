""" Download music (mp3) files from Videos of a YOUTUBE Playlist """

import os
import re
import sys
import json
import time
import random
import warnings
import requests
import urllib.request
from pathlib import Path


warnings.filterwarnings("ignore", category=DeprecationWarning)


def print_stats(video_list):
    playlist_count = video_count = 0
    print('')
    print(f'{len(video_list.keys())} playlist in total')
    for key, val in video_list.items():
        playlist_count = playlist_count + 1
        print(f'Playlist {playlist_count} - {key}: Videos {len(video_list[key])}')
        video_count = video_count + len(video_list[key])
    print(f'{video_count} videos in total')


def get_file(title, id_, my_file):
    if not Path(my_file).is_file():

        time.sleep(random.randrange(6))
        print(f'Video ID: {id_}')
        site_url = 'https://ythub.cc/download/' + id_ + '.html'
        page = requests.get(site_url)
        match_ = re.findall("u002F\?file_id=([A-Za-z0-9_-]*)\"", page.text)
        if match_:
            download_id = match_[0]

            file_url = requests.get('https://api.ythub.cc/v1/youtube/get-download-link/?file_id=' + download_id)
            response = file_url.json()

            request_url = response['dl_url']
            print(f"Download link: {request_url}")

            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                                           ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

            # Download the actual music file
            opener.retrieve(request_url, my_file)
            print(f'File Downloaded : {title}')
            print('')
        else:
            print(f'Site Overloaded | Unable to download - Video ID: {id_}')
    else:
        print(f'File already exists : {title}')


def download_music_files(video_list):
    updated_json = sys.path[0] + '/data/updated_video_list.json'
    updated_flag = False
    if Path(updated_json).is_file():
        updated_video_list = json.load(open(updated_json), )
        updated_flag = True
    else:
        updated_video_list = video_list

    print_stats(video_list)

    item = list(video_list.keys())
    for seq, m in enumerate(item):
        playlist_path = sys.path[0] + '/data/music/playlist_' + m + '/'
        print('')
        print(f'Playlist {seq + 1}: {m}')
        print('***********************')

        if not Path(playlist_path).exists():
            # Check if playlist folder exists otherwise create one
            print(f'Creating playlist folder')
            Path(playlist_path).mkdir(parents=True, exist_ok=True)

        if not updated_flag:
            # Creating the updated video list file for the first time
            updated_video_list[m] = video_list[m]
            print('Checking entire playlist videos')
            for idx, id_ in enumerate(video_list[m]):
                title = video_list[m][id_]["title"]
                my_file = playlist_path + title + '.mp3'
                get_file(title, id_, my_file)
                # Checking if file was downloaded
                if Path(my_file).is_file():
                    if os.path.getsize(my_file) <= 200:
                        # Files less than 200 kb are HTTP response with error code 400, file not found
                        download_key = 2
                        print(f'File has error code (Deleting) : {title}')
                        os.remove(my_file)
                    else:
                        download_key = 1
                    updated_video_list[m][id_]["download_key"] = download_key

        else:
            # Checking if playlists was previously downloaded
            if m not in updated_video_list:
                updated_video_list[m] = video_list[m]
                print('Downloading new playlist')
                for idx, id_ in enumerate(video_list[m]):
                    title = video_list[m][id_]["title"]
                    my_file = playlist_path + title + '.mp3'
                    get_file(title, id_, my_file)
                    # Checking if file was downloaded
                    if Path(my_file).is_file():
                        if os.path.getsize(my_file) <= 200:
                            # Files less than 200 kb are HTTP response with error code 400, file not found
                            download_key = 2
                            print(f'File has error code (Deleting) : {title}')
                            os.remove(my_file)
                        else:
                            download_key = 1
                        updated_video_list[m][id_]["download_key"] = download_key

            else:
                # Checking which video was previously downloaded
                for idx, id_ in enumerate(video_list[m]):
                    title = video_list[m][id_]["title"]
                    my_file = playlist_path + title + '.mp3'
                    if id_ not in updated_video_list[m]:
                        updated_video_list[m][id_] = video_list[m][id_]
                        get_file(title, id_, my_file)
                    else:
                        # Checking if video was downloaded earlier
                        updated_download_key = updated_video_list[m][id_]["download_key"]
                        if updated_download_key == 0:
                            # Downloading if not downloaded before
                            get_file(title, id_, my_file)
                        else:
                            # Case download_key !=1 and no file is not implemented
                            # possibility is it's downloaded before and moved (creates redundancy)
                            print(f'File previously downloaded: {title}')
                    # Checking if file was downloaded
                    if Path(my_file).is_file():
                        if os.path.getsize(my_file) <= 200:
                            # Files less than 200 kb are HTTP response with error code 400, file not found
                            download_key = 2
                            print(f'File has error code (Deleting) : {title}')
                            os.remove(my_file)
                        else:
                            download_key = 1
                        updated_video_list[m][id_]["download_key"] = download_key
    folder = 'data/'
    file = 'updated_video_list'
    ext = '.json'
    path_to_file = folder + file + ext
    outfile = open(path_to_file, 'w')
    json.dump(updated_video_list, outfile, indent=4, sort_keys=True)
    outfile.close()
