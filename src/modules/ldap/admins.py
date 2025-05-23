from rich.console import Console
console = Console()
from uuid import uuid4

class Admins:
    name = "admins"
    desc = "Get all the accounts from domain that has administrator privilege in somewhere"
    search_filter = "(&(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))(adminCount=1))"
    attributes = "sAMAccountName"

    def on_login(self, conn, base_dn, save_output: bool = False,):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)

        if not results:
            console.print("[[red]![/]] No entries found in the results.") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{self.search_filter}[/]\n", highlight=False)

        values = [entry[self.attributes].value for entry in conn.entries]
        for value in values:
            console.print(value, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)
