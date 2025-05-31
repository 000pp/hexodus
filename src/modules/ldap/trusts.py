from rich.console import Console
console = Console()
from uuid import uuid4

from helpers.values import fmt_sid

class Trusts:
    name = "Trusts"
    desc = "Enumerate the trusted domains cross the environment"
    search_filter = "(objectClass=trustedDomain)"
    attributes = [
        "cn",
        "distinguishedName",
        "objectGUID",
        "securityIdentifier",
        "trustDirection",
    ]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [black]{self.search_filter}[/]\n", highlight=False)

        trust_direction_map = {
            0: "TRUST_DIRECTION_DISABLED [0] (-)",
            1: "TRUST_DIRECTION_INBOUND [1] (->)",
            2: "TRUST_DIRECTION_OUTBOUND [2] (<-)",
            3: "TRUST_DIRECTION_BIDIRECTIONAL [3] (<->)",
        }

        values = []
        for entry in conn.entries:
            distinguishedName = entry.distinguishedName.value or "None"
            trustDirection = entry.trustDirection.value or "Unknown"
            securityIdentifier = fmt_sid(securityIdentifier) or "None"

            result = f"{distinguishedName} - {trustDirection} - {securityIdentifier}"
            values.append(result)

            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values