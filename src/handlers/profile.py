from os import environ
from json import load
from rich.console import Console
console = Console()

from handlers.environment import user_home

def get_username() -> str:
    """ Read the 'username' property from the current profile file """

    profile = environ.get('hexodus_profile')
    profile_path: str = f"{user_home()}/.hexodus/{profile}/profile.json"

    try:
        with open(profile_path, 'r', encoding='utf-8') as json_file:
            data = load(json_file)
            return data['username']

    except Exception as error:
        console.print(f"[[red]x[/]] Error when running get_username function in profile.py: {error}")

def get_password() -> str:
    """ Read the 'password' property from the current profile file """

    profile = environ.get('hexodus_profile')
    profile_path: str = f"{user_home()}/.hexodus/{profile}/profile.json"

    try:
        with open(profile_path, 'r', encoding='utf-8') as json_file:
            data = load(json_file)
            return data['password']

    except Exception as error:
        console.print(f"[[red]x[/]] Error when running get_password function in profile.py: {error}")

def get_domain() -> str:
    """ Read the 'domain' property from the current profile file """

    profile = environ.get('hexodus_profile')
    profile_path: str = f"{user_home()}/.hexodus/{profile}/profile.json"

    try:
        with open(profile_path, 'r', encoding='utf-8') as json_file:
            data = load(json_file)
            return data['domain']

    except Exception as error:
        console.print(f"[[red]x[/]] Error when running get_domain function in profile.py: {error}")