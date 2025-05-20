import ldap3
import ssl
from ldap3.core.exceptions import LDAPBindError
from rich.console import Console

console = Console()

def get_ldap_connection(host: str, username: str, password: str, domain: str):
    """ LDAP Connection Handler: tries signing on 389, then LDAPS on 636. """

    user = f"{domain}\\{username}"

    if len(password) == 32 and all(c in "0123456789abcdefABCDEF" for c in password):
        password = f"aad3b435b51404eeaad3b435b51404ee:{password}"

    tls = ldap3.Tls(validate=ssl.CERT_NONE,
                    version=ssl.PROTOCOL_TLSv1_2,
                    ciphers="ALL:@SECLEVEL=0")
    ldaps_server = ldap3.Server(f"ldaps://{host}", port=636,
                         use_ssl=True, get_info=ldap3.ALL, tls=tls)

    ldap_server = ldap3.Server(f"ldap://{host}", port=389,
                              use_ssl=False, get_info=ldap3.ALL)

    try:
        ldap_connection = ldap3.Connection(
            server=ldap_server,
            user=user,
            password=password,
            authentication=ldap3.NTLM,
            auto_bind=True,
            session_security="ENCRYPT", # ← enable LDAP signing
            raise_exceptions=True
        )

        signing = "[green]Yes[/]" if ldap_connection.session_security in ("SIGNATURE", "ENCRYPT") else "[red]No[/]"
        encrypted = "[green]Yes[/]" if ldap_connection.server.ssl else "[red]No[/]"
        base_dn = ldap_connection.server.info.other.get("defaultNamingContext", ["<none>"])[0]

        console.print(f"[[green]+[/]] [cyan]LDAP[/]   {host} " f"(Base DN: {base_dn}) " f"(Signing: {signing}) " f"(Encrypted: {encrypted})", highlight=False)
        console.print(f"[[green]+[/]] [cyan]LDAP[/]   {domain}\\{username}:{password}", highlight=False)
        console.print("[[green]+[/]] [cyan]LDAP[/]   bind successful with signing", highlight=False)

        return ldap_server, ldap_connection

    except LDAPBindError as e:
        if "strongerAuthRequired" not in str(e):
            console.print(f"[red]x[/] LDAP bind error: {e}", highlight=False)
            raise

    try:
        ldaps_connection = ldap3.Connection(
            server=ldaps_server,
            user=user,
            password=password,
            authentication=ldap3.NTLM,
            auto_bind=True,
            raise_exceptions=True
        )
        signing = "[green]Yes[/]" if ldaps_connection.session_security in ("SIGNATURE", "ENCRYPT") else "[red]No[/]"
        encrypted = "[green]Yes[/]" if ldaps_connection.server.ssl else "[red]No[/]"
        base_dn = ldaps_connection.server.info.other.get("defaultNamingContext", ["<none>"])[0]

        console.print(f"[[green]+[/]] [cyan]LDAPS[/]   {host} " f"(Base DN: {base_dn}) " f"(Signing: {signing}) " f"(Encrypted: {encrypted})", highlight=False)
        console.print(f"[[green]+[/]] [cyan]LDAPS[/]   {domain}\\{username}:{password}", highlight=False)
        console.print("[[green]+[/]] [cyan]LDAPS[/]    bind successful", highlight=False)

        return ldaps_server, ldaps_connection

    except LDAPBindError as e:
        console.print(f"[red]x[/] LDAPS bind failed: {e}", highlight=False)
        raise