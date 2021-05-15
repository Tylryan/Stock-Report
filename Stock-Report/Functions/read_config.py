#!/usr/bin/python3

import os
from dotenv import load_dotenv

# You can change this to different location if you want
env_location = '../../Data/.env'


def export_variables(env_location='../Data/.env'):
    load_dotenv(env_location)
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    return username, password


if __name__ == "__main__":
    user, passwd = export_variables()
    print(f"User: {user}")
    print(f"Password: {passwd}")
