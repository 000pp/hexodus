import ldap3
import ssl
from ldap3.core.exceptions import LDAPBindError, LDAPInvalidCredentialsResult
from rich.console import Console
from sys import exit

from handlers.profile import get_username, get_password, get_domain

console = Console()

def get_ldap_connection(host: str):
    """ LDAP Connection Handler: tries signing on 389, then LDAPS on 636. """

    username, password, domain = get_username(), get_password(), get_domain()

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
            auto_referrals=False,
            raise_exceptions=True,
            generator=True,
            paged_size=1000
        )

        signing = "[green]Yes[/]" if ldap_connection.session_security in ("SIGNATURE", "ENCRYPT") else "[red]No[/]"
        encrypted = "[green]Yes[/]" if ldap_connection.server.ssl else "[red]No[/]"
        #base_dn = ldap_connection.server.info.other.get("defaultNamingContext", ["<none>"])[0]
        base_dn = ldap_connection.server.info.naming_contexts[0]
        
        console.print(f"[[green]+[/]] [cyan]LDAP[/]    {host} " f"({base_dn}) " f"(Signing: {signing}) " f"(Encrypted: {encrypted})", highlight=False)
        console.print(f"[[green]+[/]] [cyan]LDAP[/]    {domain}\\{username}:{password}", highlight=False)
        console.print("[[green]+[/]] [cyan]LDAP[/]    bind successful with signing", highlight=False)

        return ldap_connection, base_dn

    except LDAPBindError as e:
        if "strongerAuthRequired" not in str(e):
            console.print(f"[[red]x[/]] LDAP bind error: {e}", highlight=False)
            raise

    except LDAPInvalidCredentialsResult:
        console.print(f"[[red]x[/]] Invalid credentials provided. ({user}:{password})", highlight=False)
        exit(0)

    try:
        ldaps_connection = ldap3.Connection(
            server=ldaps_server,
            user=user,
            password=password,
            authentication=ldap3.NTLM,
            auto_bind=True,
            auto_referrals=False,
            raise_exceptions=True,
            generator=True,
            paged_size=1000
        )

        signing = "[green]Yes[/]" if ldaps_connection.session_security in ("SIGNATURE", "ENCRYPT") else "[red]No[/]"
        encrypted = "[green]Yes[/]" if ldaps_connection.server.ssl else "[red]No[/]"
        base_dn = ldaps_connection.server.info.other.get("defaultNamingContext", ["<none>"])[0]

        console.print(f"[[green]+[/]] [cyan]LDAPS[/]    {host} " f"({base_dn}) " f"(Signing: {signing}) " f"(Encrypted: {encrypted})", highlight=False)
        console.print(f"[[green]+[/]] [cyan]LDAPS[/]    {domain}\\{username}:{password}", highlight=False)
        console.print("[[green]+[/]] [cyan]LDAPS[/]     bind successful", highlight=False)

        return ldap_connection, base_dn
    
    except LDAPInvalidCredentialsResult:
        console.print(f"[[red]x[/]] Invalid credentials provided. ({user}:{password})", highlight=False)
        exit(0)

    except LDAPBindError as e:
        console.print(f"[[red]x[/]] LDAPS bind failed: {e}", highlight=False)
        raise