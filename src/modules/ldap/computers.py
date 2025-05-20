from rich.console import Console
console = Console()
from uuid import uuid4

class Computers:
    name = "computers"
    desc = "Return all the computers that can be located"
    module_protocol = ["ldap"]
    opsec_safe = True
    multiple_hosts = False
    user_target = None
    search_filter = ("(&(objectClass=computer)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))")
    requires_args = False
    attributes = "dNSHostName"

    def on_login(self, conn, base_dn, save_output: bool = False):
        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)

        if not results:
            console.print("[[red]![/]] No entries found in the results.") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]  {self.search_filter}", highlight=False)

        values = [entry[self.attributes].value for entry in conn.entries]
        for value in values:
            console.print(value, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)
