from rich.console import Console
console = Console()
from uuid import uuid4
from os import makedirs, path
from shutil import rmtree
from pathlib import Path
from json import dump


def environment_json(profile_name: str, profile_domain: str, profile_username: str, profile_password: str) -> None:
    """ Create the profile data JSON file to be used by MySQL, Django services and other functions """

    profile_name = profile_name
    profile_path: str = f"{user_home()}/.hexodus/{profile_name}"
    profile_uuid = uuid4().hex

    profile_data = {
        "name": profile_name,
        "uuid": profile_uuid,
        "username": profile_username,
        "password": profile_password,
        "domain": profile_domain,
    }

    try:
        with open(f"{profile_path}/profile.json", "w", encoding="utf-8") as json_file:
            dump(profile_data, json_file, ensure_ascii=False, indent=4)

    except Exception as error:
        console.print(f"[[red][x][/]] Error when creating the profile JSON: {error}")
        return False


def list_profiles() -> None:
    """ List existent profiles based in hexodus directory """

    profile_path: str = f"{user_home()}/.hexodus/"
    folders = [folder for folder in Path(profile_path).iterdir() if folder.is_dir()]

    if not folders:
        console.print(f"[[red]x[/]] No profiles found in {profile_path}", highlight=False)
        return False
    
    for folder in folders:
        console.print(f"* {folder}", highlight=False)
    

def delete_profile(profile_name: str) -> None:
    """ Delete target profile directory """

    profile_path: str = f"{user_home()}/.hexodus/{profile_name}"

    if not path.exists(profile_path):
        console.print(f"[[red]x[/]] {profile_path} does not exists.", highlight=False)
        return False
    
    rmtree(profile_path)
    console.print(f"[[green]![/]] {profile_path} deleted.", highlight=False)
    

def create_profile(profile_name: str, profile_domain: str, profile_username: str, profile_password: str) -> None:
    """ Receive 5 string arguments to create a new profile and an JSON file """

    profile_path: str = f"{user_home()}/.hexodus/{profile_name}"
    if not path.exists(profile_path):
        makedirs(profile_path)
        console.print(f"[[green]![/]] {profile_path} created.", highlight=False)
        environment_json(profile_name, profile_domain, profile_username, profile_password)
    else:
        console.print(f"[[red]x[/]] {profile_path} already exists, use another name for the profile.", highlight=False)
        return False


def user_home() -> str:
    """ Return user's home directory as string """

    return str(Path.home())


def ensure_base_dir() -> None:
    """ Ensures hexodus directory exists in users's home """

    base_path = f"{user_home()}/.hexodus"
    if not path.exists(base_path):
        makedirs(base_path)