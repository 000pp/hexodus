from impacket.dcerpc.v5 import transport, srvs
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.smbconnection import SMBConnection
from rich.console import Console
console = Console()

from handlers.profile import get_username, get_password, get_domain

def get_rpc_connection(host: str):
        
        username, password, domain = get_username(), get_password(), get_domain()

        if len(password) == 32 and all(c in "0123456789abcdefABCDEF" for c in password):
            use_ntlmv2_hash = True
        else:
            use_ntlmv2_hash = False

        rpc_string = r"ncacn_np:%s[\pipe\srvsvc]" % host
        transport_obj = transport.DCERPCTransportFactory(rpc_string)

        if use_ntlmv2_hash:
            smb_connection = SMBConnection(host, host)
            lmhash = 'aad3b435b51404eeaad3b435b51404ee'
            nthash = password
            smb_connection.login(username, '', domain=domain, lmhash=lmhash, nthash=nthash)
            transport_obj.set_smb_connection(smb_connection)
        else:
            transport_obj.set_credentials(username, password, domain)

        try:
            transport_obj.connect()
            dce = transport_obj.DCERPC_class(transport_obj)
            dce.bind(srvs.MSRPC_UUID_SRVS)
            return dce

        except DCERPCException as error:
            console.print(f"[[red]![/]] Error estabilishing RPC connection: {error}")
            return None