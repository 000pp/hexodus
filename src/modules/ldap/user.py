from rich.console import Console
console = Console()
from uuid import uuid4

from src.parsers.formatters import fmt_multi, fmt_uac

class User:
    name = "user"
    desc = "Get information from the user specified"
    attributes = [
        "description",
        "memberOf",
        "userAccountControl",
        "badPwdCount",
        "lastLogoff",
        "lastLogon",
        "objectSid",
        "adminCount",
        "accountExpires",
        "sAMAccountName",
        "servicePrincipalName"
    ]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        if not module_args or len(module_args) == 0:
            console.print("\n[[red]![/]] You need to specify a username. Example: hexodus <profile> ldap <host> user [yellow]Administrator[/]", highlight=False)
            return

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        username = " ".join(module_args)
        search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
        results = conn.search(base_dn, search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{search_filter}[/]\n", highlight=False)

        values = []
        for entry in conn.entries:
            description = entry.description.value or "No description"
            memberOf = fmt_multi(entry.memberOf.value)
            objectSid = entry.objectSid.value or "None"
            sAMAccountName = entry.sAMAccountName.value or "None"
            accountExpires = entry.accountExpires.value or "None"
            servicePrincipalName = entry.servicePrincipalName.value or "None"
            badPwdCount = entry.badPwdCount.value
            lastLogon = entry.lastLogon.value or "None"
            lastLogoff = entry.lastLogoff.value or "None"
            userAccountControl = fmt_uac(entry.userAccountControl.value) or entry.userAccountControl.value or "None"

            result = f"""Username: {sAMAccountName}
Description: {description}
Member of: {memberOf}
SID: {objectSid}
Account Expires: {accountExpires}
servicePrincipalName: {servicePrincipalName}
badPwdCount: {badPwdCount}
Last Logon: {lastLogon}
Last Logoff: {lastLogoff}
userAccountControl: {userAccountControl}"""
            
            values.append(result)
            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
