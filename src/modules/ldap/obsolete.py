from rich.console import Console
console = Console()
from uuid import uuid4

class Obsolete:
    name = "obsolete"
    desc = "Search for computers with obsolete operating systems"
    search_filter = (
        "(&(objectclass=computer)(!(userAccountControl:1.2.840.113556.1.4.803:=2))"
        "(|(operatingSystem=*Windows 6*)(operatingSystem=*Windows 2000*)"
        "(operatingSystem=*Windows XP*)(operatingSystem=*Windows Vista*)"
        "(operatingSystem=*Windows 7*)(operatingSystem=*Windows 8*)"
        "(operatingSystem=*Windows 8.1*)(operatingSystem=*Windows Server 2003*)"
        "(operatingSystem=*Windows Server 2008*)(operatingSystem=*Windows Server 2000*)))"
    )
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
            sAMAccountName = entry.sAMAccountName.value or "None"
            operatingSystem = entry.operatingSystem.value or "None"
            dNSHostName = entry.dNSHostName.value or "None"

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
