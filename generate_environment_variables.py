""" Generates environment variables for the entire application from config """

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv


def load_json_file(file_name):
    """
    It loads the json file data
    :param file_name: takes name of json file as parameter to load data
    :return: return variable with loaded json data
    """

    folder = '/config/'
    ext = '.json'
    path_to_file = sys.path[0] + folder + file_name + ext
    try:
        json_data = open(path_to_file, )
        data = json.load(json_data)
        json_data.close()
    except IOError as e:
        print(f'Error: {e}, File "{file_name}{ext}" does not appear to exist.')
        sys.exit(1)
    return data


def write_authorization_data(data):
    """
    The function write Authorization environment variables to .env file
    :param data: takes json data of Authorization variables
    :return: Creates Authorization environment variables
    """
    m = list(data.keys())[0]

    env_file = open('config/.env', 'w')
    print('Writing new data to env file')

    for i in data[m]:
        # to print the configuration data
        # print(i+'='+data[m][i])
        print(i.upper())
        os.environ[i.upper()] = data[m][i]

    for i in data[m]:
        env_file.write(i.upper() + '=' + os.environ.get(i.upper()) + '\n')
    env_file.close()


def write_api_data(data):
    """
    The function write API environment variables to .env file
    :param data: takes json data of API variables
    :return: Creates API environment variables
    """
    env_file = open('config/.env', 'a')
    print('Appending API data to env file')

    for i in data:
        # to print the configuration data
        # print(i + '=' + data[i])
        print(i.upper())
        os.environ[i.upper()] = data[i]

    for i in data:
        env_file.write(i.upper() + '=' + os.environ.get(i.upper()) + '\n')
    env_file.close()


def json_to_env():
    """
    The function generate environment variables from the existing API and Authorization json files
    :return: Creates .env file in the config folder with environment variables
    """
    file_name = 'authorization'
    auth_data = load_json_file(file_name)
    write_authorization_data(auth_data)
    file_name = 'api'
    api_data = load_json_file(file_name)
    write_api_data(api_data)


def truncate_file():
    """
    The function clear the existing data from environment variable file
    :return: Empty file
    """
    print('Clearing data from existing file')
    env_file = open('config/.env', 'w')
    env_file.truncate()


def testing_loaded_data():
    """
    The function check the existence of environment variables in the application
    :return: Prints PASSED or FAILED output
    """
    print('Testing Authorization Variable - AUTH_URI:')
    if os.environ.get('AUTH_URI'):
        print(os.environ.get('AUTH_URI'))
        print('PASSED')
    else:
        print('FAILED')
        print('Authorization Environment variable failed to load')

    print('Testing API Variable - YOUTUBE_API_SERVICE_NAME:')
    if os.environ.get('YOUTUBE_API_SERVICE_NAME'):
        print(os.environ.get('YOUTUBE_API_SERVICE_NAME'))
        print('PASSED')
    else:
        print('FAILED')
        print('API Environment variable failed to load')


def load_env_variables(clear_env_file=0):
    """
    The function checks for existing data in environment file otherwise generates one
    :param clear_env_file: Take the user input as non zero to truncate existing environment variable file
    :return: loads all the environment variables to .env file
    """

    if clear_env_file != 0:
        truncate_file()

    # Validation Check: if the file exists and has data
    if Path(sys.path[0] + '/config/.env').exists() and os.path.getsize(sys.path[0] + '/config/.env'):
        load_dotenv(sys.path[0] + '/config/.env')
        print('Environment variables loaded from existing file')
    else:
        json_to_env()

    # Testing of loaded variables
    testing_loaded_data()
