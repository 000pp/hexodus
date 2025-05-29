from rich.console import Console
console = Console()
from uuid import uuid4
from impacket.dcerpc.v5 import srvs

from protocols.rpc import get_rpc_connection

class Share:
    name = "share"
    desc = "Enumerates the available shares of a target computer"

    def on_login(self, host, save_output = False, module_args = None):

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        rpc_connection = get_rpc_connection(host)
        resp = srvs.hNetrShareEnum(rpc_connection, 2)

        if rpc_connection is None:
                console.print(f"[[red]![/]] Unable to estabilish RPC connection with {host}")
                return

        if resp is None or resp["ErrorCode"] != 0:
            console.print("[[red]![/]] Error enumerating share information")
            return
        
        output = []

        for share in resp["InfoStruct"]["ShareInfo"]["Level2"]["Buffer"]:
            share_name = share["shi2_netname"][:-1]
            share_remark = share["shi2_remark"][:-1]
            share_path = share["shi2_path"][:-1]

            share_info: str = f"{share_name} - {share_remark} - {share_path}"
            
            console.print(f" * {share_info} ", highlight=False)

            output.append(share_info)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                for value in output:
                    file.write(value + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return output
