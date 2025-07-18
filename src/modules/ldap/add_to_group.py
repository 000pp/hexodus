from rich.console import Console
console = Console()
from uuid import uuid4
from ldap3 import MODIFY_ADD
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult, LDAPEntryAlreadyExistsResult

from protocols.ldap import safe_ldap_attr

class Add_to_group:
    name = "addtogroup"
    desc = "Add user to a desired group"

    def get_user_dn(self, conn, base_dn, user):
        conn.search(base_dn, f"(&(objectClass=user)(sAMAccountName={user}))", attributes=["distinguishedName"])
        for entry in conn.entries:
            user_dn = safe_ldap_attr(entry, 'distinguishedName', 'None')
            return str(user_dn)

    def get_group_dn(self, conn, base_dn, group):
        conn.search(base_dn, f"(&(objectClass=group)(cn={group}))", attributes=["distinguishedName"])
        for entry in conn.entries:
            group_dn = safe_ldap_attr(entry, 'distinguishedName', 'None')
            return str(group_dn)

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        if not module_args or len(module_args) < 2:
            console.print("\n[[red]![/]] You need to specify a username and a grouop. Example: hexodus <profile> ldap <host> user [yellow]Administrator[/] [yellow]'Domain Admins'[/]", highlight=False)
            return

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        username = module_args[0]
        group = module_args[1]

        user_dn = self.get_user_dn(conn, base_dn, username)
        group_dn = self.get_group_dn(conn, base_dn, group)

        console.print(f"\n[[yellow]![/]] Adding {username} to {group} group", highlight=False)

        try:
            add_to_group = conn.modify(group_dn, {"member": [(MODIFY_ADD, [user_dn])]})

        except LDAPEntryAlreadyExistsResult:
            console.print(f"[[yellow]![/]] {username} is already a member of {group} group", highlight=False)
            return

        except LDAPInsufficientAccessRightsResult:
            console.print(f"[[red]x[/]] You don't have enough privileges to add {username} to {group} group", highlight=False)
            return


        values = []
        result = f"{username} added to {group} successfully"
        console.print(result, highlight=False)
        values.append(result)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
