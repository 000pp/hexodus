from importlib import resources, import_module
from rich.console import Console
console = Console()
from argparse import ArgumentParser, REMAINDER
from os import environ, path

from handlers.environment import *
from protocols.smb import get_smb_connection
from protocols.ldap import get_ldap_connection
from webapp import start_flask, stop_flask

from sys import argv

def setup() -> None:
    """
    Initialize and manage the Hexodus environment and CLI operations.
    """

    parser = ArgumentParser(
        description="To list modules from a protocol use: hexodus <profile> <protocol> list"
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

    parser.add_argument(
        "module_args",
        help="Arguments specific to the chosen module",
        nargs='*',
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
        "--list-profiles", "-lp",
        help="Usage: hexodus --list-profiles",
        action="store_true"
    )

    # Save the output of the command
    parser.add_argument(
        "--output", "-o",
        help="Usage: hexodus <profile> <protocol> <host> <module> --output",
        action="store_true"
    )

    # Generate a web view of the collected data
    parser.add_argument(
        "--start-web", "-s",
        help="Usage: hexodus --start-web",
        action="store_true"
    )

    # Stop the Flask web app
    parser.add_argument(
        "--stop-web", "-sw",
        help="Usage: hexodus --stop-web",
        action="store_true"
    )

    # Delete the profile column from the data.db file
    parser.add_argument(
        "--delete-profile-column", "-x",
        metavar="PROFILE_NAME",
        help="Usage: hexodus --delete-profile-column <profile-name>",
        type=str,
    )

    args = parser.parse_args()
    save_output = args.output
    ensure_base_dir()
    
    if args.create_profile:
        create_profile(*args.create_profile)

    if args.delete_profile:
        delete_profile(args.delete_profile)

    if args.list_profiles:
        list_profiles()
        return
    
    if args.start_web:
        start_flask()
        return

    if args.stop_web:
        stop_flask()
        return
    
    if args.delete_profile_column:
        drop_profile_column(args.delete_profile_column)
        return

    if args.profile:
        # Check if profile exists before loading it
        profile_path: str = f"{user_home()}/.hexodus/{args.profile}"
        if not path.exists(profile_path):
            console.print(f"[[red]x[/]] {args.profile} does not exists.", highlight=False)
            return
        
        environ['hexodus_profile'] = args.profile
        init_database()
        ensure_profile_column(args.profile)

        if args.profile and args.protocol is None:
            console.print(f"[[green]+[/]] Loaded profile: {environ['hexodus_profile']}")
            return

        if args.protocol == "smb":

            if args.module == None and args.host == None:
                console.print("[[red]![/]] You need to specify at least one host address")
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
                    values = instance.on_login(args.host, save_output, args.module_args)

                    if values:
                        text = "\n".join(values)
                        save_to_database(args.profile, args.module, text)

                except ModuleNotFoundError:
                    raise Exception
                    console.print(f"\n[[red]x[/]] Module '{args.module}' not found")
                    return


        if args.protocol == "ldap":

            if args.module == None and args.host == None:
                console.print("[[red]x[/]] You need to specify at least one host address")
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
                    values = instance.on_login(conn, base_dn, save_output, args.module_args)

                    if values:
                        text = "\n".join(values)
                        save_to_database(args.profile, args.module, text)

                except ModuleNotFoundError:
                    raise Exception
                    console.print(f"\n[[red]x[/]] Module '{args.module}' not found")
                    return