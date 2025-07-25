from rich.console import Console
console = Console()
from uuid import uuid4

class Users:
    name = "users"
    desc = "Get 'sAMAccountName' attribute value from Users Accounts"
    search_filter = "(&(objectCategory=person)(objectClass=user))"
    attributes = "sAMAccountName"

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [white]{self.search_filter}[/]\n", highlight=False)

        try:
            generator = conn.extend.standard.paged_search(
                search_base=base_dn,
                search_filter=self.search_filter,
                search_scope='SUBTREE',
                attributes=[self.attributes],
                paged_size=1000,
                generator=True
            )

            values = []
            for entry in generator:
                if entry.get('type') != 'searchResEntry':
                    continue

                username_attribute = entry.get('attributes', {}).get(self.attributes)
                if not username_attribute:
                    continue

                value = username_attribute[0] if isinstance(username_attribute, list) else username_attribute
                values.append(value)
                console.print(value, highlight=False)
            
            if not values:
                console.print(f"\n[[red]![/]] No results for {self.name}") 
                return
            
            if save_output:
                filename = f"{self.name}_{uuid4().hex}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for v in values:
                        f.write(v + "\n")
                console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

            return values
        
        except Exception as error:
            console.print(f"[[red]![/]] Error in users.py module: {error}", highlight=False)
            raise