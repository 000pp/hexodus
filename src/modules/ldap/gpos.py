from rich.console import Console
console = Console()
from uuid import uuid4

class Gpos:
    name = "gpos"
    desc = "List the GPOs registed in the domain"
    search_filter = "(objectClass=groupPolicyContainer)"
    attributes = ["displayName", "gPCFileSysPath"]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{self.search_filter}[/]\n", highlight=False)

        values = []
        values = []
        for entry in conn.entries:
            displayName = entry.displayName.value or "None"
            gPCFileSysPath = entry.gPCFileSysPath.value or "None"

            result = f"{displayName} - {gPCFileSysPath}"
            values.append(result)

            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
