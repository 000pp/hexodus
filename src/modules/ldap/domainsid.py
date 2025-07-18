from rich.console import Console
console = Console()
from uuid import uuid4
from ldap3 import SUBTREE

from protocols.ldap import safe_ldap_attr

class Domainsid:
    name = "domainsid"
    desc = "Get SID value from Domain Controllers"
    search_filter = "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))"
    attributes = ["cn", "objectSid", "dNSHostName"]

    def search_with_base(self, conn, search_base, search_filter, attributes, scope):
        return conn.search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=scope,
            attributes=attributes,
        )

    def on_login(self, conn, base_dn, save_output=False, module_args=None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = self.search_with_base(
            conn,
            search_base=base_dn,
            search_filter=self.search_filter,
            attributes=self.attributes,
            scope=SUBTREE,
        )

        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [white]{self.search_filter}[/]\n", highlight=False)

        values = []
        for entry in entries:
            dNSHostName = safe_ldap_attr(entry, 'dNSHostName', 'None')
            objectSid = safe_ldap_attr(entry, 'objectSid', 'None')
            cn = safe_ldap_attr(entry, 'cn', 'None')

            result = f"{dNSHostName} - {objectSid} - {cn}"
            console.print(result, highlight=False)

            values.append(result)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
