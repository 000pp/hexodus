from impacket.smbconnection import SMBConnection, SessionError
from rich.console import Console
console = Console()

from handlers.profile import get_host, get_username, get_password, get_domain

def get_smb_connection() -> None:
    """ SMB Connection Handler """

    host, username, password, domain = get_host(), get_username(), get_password(), get_domain()

    try:
        smb_connection = SMBConnection(host, host)

        if len(password) == 32 and all(c in "0123456789abcdefABCDEF" for c in password):
            lmhash = "aad3b435b51404eeaad3b435b51404ee"
            nthash = password
            smb_connection.login(username, '', lmhash=lmhash, nthash=nthash)
        else:
            smb_connection.login(username, password, domain)

        smb_name = smb_connection.getServerDNSHostName()
        smb_os = smb_connection.getServerOS()
        smb_ntlmv2_support: bool = '[green]True[/]' if smb_connection.doesSupportNTLMv2() else '[red]False[/]'
        smb_signing_required: bool = '[green]True[/]' if smb_connection.isSigningRequired() else '[red]False[/]'

        console.print(f"[[green]+[/]] [cyan]SMB[/]   {host} {smb_os} (Name: {smb_name}) (Signing: {smb_signing_required}) (NTLMv2: {smb_ntlmv2_support})", highlight=False)
        console.print(f"[[green]+[/]] [cyan]SMB[/]   {domain}\\{username}:{password}", highlight=False)

        return smb_connection
    
    except SessionError as session_error:
        if "STATUS_LOGON_FAILURE" in str(session_error):
            console.print(f"[[red]x[/]] Invalid credentials: [cyan]SMB[/] {host} {domain}\\{username}:{password}", highlight=False)
        return None

    except Exception as error:
        console.print(f"[[red]x[/]] Error establishing SMB connection: {error}", highlight=False)
        return None   