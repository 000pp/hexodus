from rich.console import Console
console = Console()
from uuid import uuid4

class Search_computer:
    name = "searchcomputer"
    desc = "Get information from the group name specified"
    attributes = ["dNSHostName"]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        if not module_args or len(module_args) == 0:
            console.print("\n[[red]![/]] You need to specify a group name. Example: hexodus <profile> ldap <host> searchcomputer [yellow]'SRVWEB'[/]", highlight=False)
            return

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        computer_name = " ".join(module_args)
        search_filter = f"(&(objectCategory=computer)(cn=*{computer_name}*))"
        results = conn.search(base_dn, search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{search_filter}[/]\n", highlight=False)

        values = []
        for entry in conn.entries:
            dNSHostName = entry.dNSHostName.value or "None"
            
            values.append(dNSHostName)
            console.print(dNSHostName, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
