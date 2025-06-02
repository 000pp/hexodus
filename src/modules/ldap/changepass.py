from rich.console import Console
console = Console()
from uuid import uuid4
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult

class Changepass:
    name = "changepass"
    desc = "Change desired user password"
    attributes = ["sAMAccountName"]

    def get_user_dn(self, conn, base_dn, user):
        conn.search(base_dn, f"(&(objectClass=user)(sAMAccountName={user}))", attributes=["distinguishedName"])
        for entry in conn.entries:
            user_dn = entry.distinguishedName.value or "None"
            return str(user_dn)

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        if not module_args or len(module_args) < 2:
            console.print("\n[[red]![/]] You need to specify a username and a password. Example: hexodus <profile> ldap <host> user [yellow]Administrator[/] [yellow]NewPass123[/]", highlight=False)
            return

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        username = module_args[0]
        password = module_args[1]
        user_dn = self.get_user_dn(conn, base_dn, username)
        
        if user_dn == "None":
            console.print(f"\n[[red]x[/]] Impossible to get {username} distinguishedName attribute value. Check if the user actually exists.")
            return
        
        console.print(f"\n[black]{username} distinguishedName: {user_dn}[/]", highlight=False)
        console.print(f"[[yellow]![/]] Changing {username} password to {password}", highlight=False)

        try:
            change_pass = conn.extend.microsoft.modify_password(user=user_dn, new_password=password, old_password=None)

            if not(change_pass):
                console.print(f"[[red]x[/]] Unable to change {username} password to {password}", highlight=False)
                return

        except LDAPInsufficientAccessRightsResult:
            console.print(f"[[red]x[/]] You don't have enough privileges to change [b]{username}[/] password", highlight=False)
            return

        values = []
        result = f"{username}'s password changed to {password} successfully"
        console.print(result, highlight=False)
        values.append(result)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
