from rich.console import Console
console = Console()
from uuid import uuid4

class Users:
    name = "users"
    desc = "Get 'sAMAccountName' attribute value from Users Accounts"
    search_filter = "(&(objectCategory=person)(objectClass=user))"
    attributes = "sAMAccountName"

    def on_login(self, conn, base_dn, save_output: bool = False):

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
