from rich.console import Console
console = Console()
from uuid import uuid4

from parsers.formatters import fmt_multi

class Group:
    name = "group"
    desc = "Get information from the group name specified"
    attributes = [
        "adminCount",
        "description",
        "distinguishedName",
        "member",
        "memberOf",
        "objectSid",
        "sAMAccountName",
    ]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        if not module_args or len(module_args) == 0:
            console.print("\n[[red]![/]] You need to specify a group name. Example: hexodus <profile> ldap <host> group [yellow]'Domain Admins'[/]", highlight=False)
            return

        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        group_name = " ".join(module_args)
        search_filter = f"(&(objectClass=group)(cn={group_name}))"
        results = conn.search(base_dn, search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{search_filter}[/]\n", highlight=False)

        values = []
        for entry in conn.entries:
            adminCount = "Yes" if entry.adminCount.value == "1" else "No" or "None"
            description = entry.description.value or "No description"
            distinguishedName = fmt_multi(entry.distinguishedName.value)
            members = fmt_multi(entry.member.value)
            memberOf = fmt_multi(entry.memberOf.value)
            objectSid = entry.objectSid.value or "None"
            sAMAccountName = entry.sAMAccountName.value or "None"

            result = f"""High Privilege Group: {adminCount}
Group Name: {sAMAccountName}
Group Description: {description}
DN: {distinguishedName}
Members: {members}
Member of: {memberOf}
SID: {objectSid}"""
            
            values.append(result)
            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
