import importlib

from rich.console import Console
console = Console()
from argparse import ArgumentParser
from sys import argv
from os import environ

from handlers.environment import ensure_base_dir, create_profile, delete_profile, list_profiles, change_host
from protocols.smb import get_smb_connection
from protocols.ldap import get_ldap_connection

def setup() -> None:
    """
    Initialize and manage the Hexodus environment and CLI operations.
    """

    parser = ArgumentParser()

    if len(argv) == 1:
        parser.print_help()
        return

    # Positional argument to be used as the PROFILE
    parser.add_argument(
        "profile",
        help="Specify the profile to be used",
        nargs="?", 
        default=None
    )

    # Positional argument to be used as the PROTOCOL
    parser.add_argument(
        "protocol",
        help="Specify the protocol to be used",
        nargs="?", 
        default=None
    )

    # Positional argument to be used as the MODULE
    parser.add_argument(
        "module",
        help="Specify the module to be used",
        nargs="?", 
        default=None
    )

    # Create profile
    parser.add_argument(
        "--create-profile",
        metavar=('PROFILE_NAME', 'PROFILE_DOMAIN', 'PROFILE_IP', 'PROFILE_USERNAME', 'PROFILE_PASSWORD'),
        help="Usage: hexodus --create-profile <profile_name> <profile_domain> <profile_ip> <profile_username> <profile_password>", 
        nargs=5, 
        default=[]
    )
    
    # Delete profile
    parser.add_argument(
        "--delete-profile",
        metavar=('PROFILE_NAME'),
        help="Usage: hexodus --delete-profile <profile_name>", 
    )

    # List profiles
    parser.add_argument(
        "--list-profiles",
        help="Usage: hexodus --list-profiles",
        action="store_true"
    )

    # Let the user change the host value from the profile
    parser.add_argument(
        "--change-host",
        metavar=('PROFILE_NAME', 'NEW_HOST'),
        help="Usage: hexodus --change-host <profile> <new_host>",
        nargs=2,
        default=[]
    )

    # Save the output of the command
    parser.add_argument(
        "--output",
        help="Usage: hexodus --output",
        action="store_true"
    )

    args = parser.parse_args()

    ensure_base_dir()
    save_output = args.output
    
    if args.create_profile:
        create_profile(*args.create_profile)

    if args.delete_profile:
        delete_profile(args.delete_profile)

    if args.list_profiles:
        list_profiles()
    
    if args.change_host:
        change_host(*args.change_host)

    if args.profile:
        environ['hexodus_profile'] = args.profile

        if args.protocol == "smb":
            get_smb_connection()

            # if args.module is True:
            #     m = importlib.import_module(f"modules.smb.{args.module}")
            #     cls = getattr(m, args.module.capitalize())
            #     instance = cls()
            #     instance.on_login(conn, base_dn)

        if args.protocol == "ldap":
            conn, base_dn = get_ldap_connection()

            if args.module:
                m = importlib.import_module(f"modules.ldap.{args.module}")
                cls = getattr(m, args.module.capitalize())
                instance = cls()
                instance.on_login(conn, base_dn, save_output)

    # Setup the MySQL database

    # Setup the Django web server