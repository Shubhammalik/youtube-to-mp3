from music_download import download_music_files
from create_youtube_list import check_and_load_data

if __name__ == '__main__':
    """
    In Check_and_load_data(), anything other than 0 will retrieve new data
    """
    download_new_data = 0
    video_list_ = check_and_load_data(download_new_data)
    download_music_files(video_list_)
