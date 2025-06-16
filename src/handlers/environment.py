from rich.console import Console
console = Console()
from uuid import uuid4
from os import makedirs, path, environ
from shutil import rmtree
from pathlib import Path
from json import dump

import sqlite3

def init_database() -> None:
    """ Initializes the default Hexodus database """
    
    database = path.join(user_home(), ".hexodus", "data.db")
    sqlite_cursor = sqlite3.connect(database)
    sqlite_cursor.execute("""
      CREATE TABLE IF NOT EXISTS data (
        module TEXT PRIMARY KEY
      );
    """)
    sqlite_cursor.commit()
    sqlite_cursor.close()


def ensure_profile_column(profile: str) -> None:
    """ Makes sure that the "profile" column exists in Hexodus database """
    
    database = path.join(user_home(), ".hexodus", "data.db")
    database_connection = sqlite3.connect(database)
    sqlite_cursor = database_connection.cursor()

    sqlite_cursor.execute("PRAGMA table_info(data);")
    existing = {row[1] for row in sqlite_cursor.fetchall()}

    if "module" not in existing:
        sqlite_cursor.execute("ALTER TABLE data ADD COLUMN module TEXT;")
        sqlite_cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_data_module ON data(module);")

    if profile not in existing:
        sqlite_cursor.execute(f"ALTER TABLE data ADD COLUMN '{profile}' TEXT;")

    database_connection.commit()
    database_connection.close()


def save_to_database(profile: str, module: str, output: str) -> None:
    """ Save the collected data to the database to be used by the webapp """

    database = f"{user_home()}/.hexodus/data.db"
    database_connection = sqlite3.connect(database)
    sqlite_cursor = database_connection.cursor()

    sqlite_cursor.execute("""
      INSERT INTO data(module) VALUES(?)
      ON CONFLICT(module) DO NOTHING
    """, (module,))

    sqlite_cursor.execute(f"""
      UPDATE data
      SET "{profile}" = ?
      WHERE module = ?
    """, (output, module))

    database_connection.commit()
    database_connection.close()


def drop_profile_column(profile_name: str) -> None:
    """ Remove the specified profile data from the database """

    database = f"{user_home()}/.hexodus/data.db"
    database_connection = sqlite3.connect(database)
    sqlite_cursor = database_connection.cursor()

    sqlite_cursor.execute(f'ALTER TABLE data DROP COLUMN "{profile_name}"')
    database_connection.commit()
    database_connection.close()


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

    drop_profile_column(profile_name)

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

    if not path.exists(f"{base_path}/data.db"):
        init_database()