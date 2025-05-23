from importlib import resources, import_module
from rich.console import Console
console = Console()
from argparse import ArgumentParser
from sys import argv
from os import environ

from handlers.environment import ensure_base_dir, create_profile, delete_profile, list_profiles
from protocols.smb import get_smb_connection
from protocols.ldap import get_ldap_connection

def setup() -> None:
    """
    Initialize and manage the Hexodus environment and CLI operations.
    """

    parser = ArgumentParser(
        description="To list modules from a protocol use: hexodus <profile> <protocol> <host> list"
    )

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

    # Positional argument to be used as the HOST
    parser.add_argument(
        "host",
        help="Specify the host to be used",
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
        "--create-profile", "-c",
        metavar=('PROFILE_NAME', 'PROFILE_DOMAIN', 'PROFILE_USERNAME', 'PROFILE_PASSWORD'),
        help="Usage: hexodus --create-profile <profile_name> <profile_domain> <profile_username> <profile_password>", 
        nargs=4, 
        default=[]
    )
    
    # Delete profile
    parser.add_argument(
        "--delete-profile", "-d",
        metavar=('PROFILE_NAME'),
        help="Usage: hexodus --delete-profile <profile_name>", 
    )

    # List profiles
    parser.add_argument(
        "--list-profiles", "-li",
        help="Usage: hexodus --list-profiles",
        action="store_true"
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

    if args.profile:
        environ['hexodus_profile'] = args.profile

        if args.profile and args.protocol is None:
            console.print(f"[[green]+[/]] Loaded profile: {environ['hexodus_profile']}")
            return


        if args.protocol == "smb":

            if args.module == None and args.host == None:
                console.print("[[red]![/]] You need to specify at least a host address")
                return

            if args.module == None and args.host != "list":
                get_smb_connection(args.host)
                return
            
            if args.host == "list":
                import modules.smb as smb_pkg
                for file in resources.files(smb_pkg).iterdir():
                    if file.suffix == ".py" and file.name != "__init__.py":
                        console.print(f"[[green]+[/]] {file.stem}")

            if args.module:
                get_smb_connection(args.host)

                try:
                    module = import_module(f"modules.smb.{args.module}")
                    cls = getattr(module, args.module.capitalize())
                    instance = cls()
                    instance.on_login(args.host, save_output)
                except ModuleNotFoundError:
                    console.print(f"[ERROR] Module '{args.module}' not found.")


        if args.protocol == "ldap":

            if args.module == None and args.host == None:
                console.print("[[red]![/]] You need to specify at least a host address")
                return

            if args.module == None and args.host != "list":
                get_ldap_connection(args.host)
                return
            
            if args.host == "list":
                import modules.ldap as ldap_pkg
                for file in resources.files(ldap_pkg).iterdir():
                    if file.suffix == ".py" and file.name != "__init__.py":
                        console.print(f"[[green]+[/]] {file.stem}")

            if args.module:
                conn, base_dn = get_ldap_connection(args.host)

                try:
                    module = import_module(f"modules.ldap.{args.module}")
                    cls = getattr(module, args.module.capitalize())
                    instance = cls()
                    instance.on_login(conn, base_dn, save_output)
                except ModuleNotFoundError:
                    console.print(f"[ERROR] Module '{args.module}' not found.")

    # Setup the MySQL database

    # Setup the Django web server