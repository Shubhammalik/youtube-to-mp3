""" Pull All Youtube Videos from a Playlist using youtube v3 API """

import os
import re
import sys
import json
import urllib.request
from pathlib import Path
from googleapiclient.discovery import build
from generate_environment_variables import load_env_variables

"""
Loading environment variables, pass 1 in the function to re-create env file
"""
load_env_variables(0)
CHANNEL_ID = os.environ.get('CHANNEL_ID')
DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = os.environ.get('YOUTUBE_API_SERVICE_NAME')
YOUTUBE_API_VERSION = os.environ.get('YOUTUBE_API_VERSION')


def fetch_all_videos(playlistId):
    """
    Fetches a playlist of videos from youtube
    :param playlistId: (string) Id of channel's playlist
    :return: playListItem Dict
    """

    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    res = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while 'nextPageToken' in res:
        nextPage = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            maxResults="50",
            pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res


def get_video_list(playlist_id):
    """
    The function gets all the videos from public playlist, limits the data to 32 videos
    :param playlist_id: youtube playlist ID
    :return: list of all videos in a playlist
    """
    html = urllib.request.urlopen("https://www.youtube.com/watch?v=&list=" + playlist_id + "&index=1")
    video_ids = re.findall(r"r\":{\"videoId\":\"(\S{11})", html.read().decode())
    print(len(video_ids))
    print(video_ids)
    return video_ids


def get_playlist_ids(channelId):
    """
    Fetches a list of all public playlist of any channel
    :param channelId: Unique channel id from youtube
    :return: list of all public playlists of that channel
    """
    search_keyword = channelId + "/playlists"
    html = urllib.request.urlopen("https://www.youtube.com/channel/" + search_keyword)

    playlist_id = re.findall(r",\"playlistId\":\"([A-Za-z0-9_-]*)", html.read().decode())

    playlist_list = list(set(playlist_id))
    print(f'{len(playlist_list)} playlists in total')
    return playlist_list


def retrieve_all_data(print_data=0):
    """
    Fetches entire youtube channel data including all public playlists and videos
    :param print_data: takes in value 0 or any number to print fetched data
    :return: write the data to a json file with videoID and title
    """
    print('')
    print('Fetching data and generating new data file')
    video_list = {}
    playlist_ = get_playlist_ids(CHANNEL_ID)
    for i, playlist in enumerate(playlist_):
        data = fetch_all_videos(playlist)
        video_list[playlist] = {}
        for idx, item in enumerate(data['items']):
            video_list[playlist][item['snippet']['resourceId']['videoId']] = {}
            title = str(item['snippet']['title']).replace('/', ' ')
            video_list[playlist][item['snippet']['resourceId']['videoId']]['title'] = title
            video_list[playlist][item['snippet']['resourceId']['videoId']]['download_key'] = 0

    if print_data != 0:
        playlist_count = video_count_ = 0
        for key, val in video_list.items():
            playlist_count = playlist_count + 1
            print(f'Playlist {playlist_count} - {key}: Videos {len(video_list[key])}')
            video_count_ = video_count_ + len(video_list[key])
        print(f'{video_count_} videos in total')
        item = list(video_list.keys())
        for seq, m in enumerate(item):
            print('')
            print(f'Playlist {seq + 1}: {m}')
            print('***********************')
            for idx, item in enumerate(video_list[m]):
                print(f'{str(idx + 1)} : {item} {video_list[m][item]}')

    if not Path(sys.path[0] + '/data/').exists():
        Path(sys.path[0] + '/data/').mkdir(parents=True, exist_ok=True)
    folder = 'data/'
    file = 'video_list'
    ext = '.json'
    path_to_file = folder + file + ext
    outfile = open(path_to_file, 'w')
    json.dump(video_list, outfile, indent=4, sort_keys=True)
    outfile.close()


def check_and_load_data(download_new_data=0):
    """
    The function check for existing data file or generate a new one
    :param download_new_data: Takes parameter 0 or any number to download new data file
    :return: returns a list of all videos of a channel's all playlists
    """
    folder = 'data/'
    file = 'video_list'
    ext = '.json'
    path_to_file = folder + file + ext
    if download_new_data != 0:
        retrieve_all_data(print_data=1)
    elif not Path(sys.path[0] + '/' + path_to_file).exists() \
            or not os.path.getsize(sys.path[0] + '/' + path_to_file):
        retrieve_all_data(print_data=1)
    else:
        pass
    video_list_ = json.load(open(path_to_file), )
    return video_list_
