from rich.console import Console
console = Console()
from uuid import uuid4

from protocols.ldap import safe_ldap_attr

class Servers:
    name = "servers"
    desc = "Get 'sAMAccountName', 'operatingSystem' and 'dnsHostName' from all Windows Servers"
    search_filter = "(&(objectCategory=computer)(operatingSystem=*server*))"
    attributes = ["sAMAccountName", "operatingSystem", "dNSHostName"]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{self.search_filter}[/]\n", highlight=False)

        values = []
        for entry in conn.entries:
            sAMAccountName = safe_ldap_attr(entry, 'sAMAccountName', 'None')
            operatingSystem = safe_ldap_attr(entry, 'operatingSystem', 'None')
            dNSHostName = safe_ldap_attr(entry, 'dNSHostName', 'None')

            result = f"{sAMAccountName} - {operatingSystem} - {dNSHostName}"
            values.append(result)

            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                for value in values:
                    file.write(value + "\n")

            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
