from rich.console import Console
console = Console()
from uuid import uuid4

from parsers.formatters import fmt_sid
from protocols.ldap import safe_ldap_attr, safe_ldap_sid

class Trusts:
    name = "trusts"
    desc = "Get Domain Trusts"
    search_filter = "(objectClass=trustedDomain)"
    attributes = ["cn", "distinguishedName", "securityIdentifier", "trustDirection", "trustType"]

    def on_login(self, conn, base_dn, save_output = False, module_args = None):
        console.print(f"[[green]+[/]] [cyan]MODULE[/]  Running [yellow]{self.name}[/] module")

        results = conn.search(base_dn, self.search_filter, attributes=self.attributes)
        entries = conn.entries

        if not entries:
            console.print(f"\n[[red]![/]] No results for {self.name}") 
            return
        
        console.print(f"[[green]+[/]] [cyan]QUERY[/]   [white]{self.search_filter}[/]\n", highlight=False)

        # Source: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/5026a939-44ba-47b2-99cf-386a9e674b04

        def fmt_trust_direction(direction):
            trust_direction_map = {
                0: "TRUST_DIRECTION_DISABLED [0] (-)",
                1: "TRUST_DIRECTION_INBOUND [1] (->)",
                2: "TRUST_DIRECTION_OUTBOUND [2] (<-)",
                3: "TRUST_DIRECTION_BIDIRECTIONAL [3] (<->)",
            }

            for value, description in trust_direction_map.items():
                if direction == value:
                    return str(description)
                
        def fmt_trust_type(type):
            trust_type_map = {
                1: "The trusted domain is a Windows domain not running Active Directory",
                2: "The trusted domain is a Windows domain running Active Directory",
                3: "The trusted domain is running a non-Windows, RFC4120-compliant Kerberos distribution",
                4: "Historical reference; this value is not used in Windows",
                5: "The trusted domain is in Azure Active Directory",
            }

            for value, description in trust_type_map.items():
                if type == value:
                    return str(description)

        values = []
        for entry in conn.entries:
            cn = safe_ldap_attr(entry, 'cn', 'None')
            distinguishedName = safe_ldap_attr(entry, 'distinguishedName', 'None')
            securityIdentifier = safe_ldap_sid(entry, 'securityIdentifier', 'None')

            raw_direction = safe_ldap_attr(entry, 'trustDirection', None)
            if raw_direction is not None:
                trustDirection = fmt_trust_direction(raw_direction)
            else:
                trustDirection = 'None'

            raw_type = safe_ldap_attr(entry, 'trustType', None)
            if raw_type is not None:
                trustType = fmt_trust_type(raw_type)
            else:
                trustType = 'None'

            result = f"""cn: {cn}
distinguishedName: {distinguishedName}
SID: {securityIdentifier}
Trust Direction: {trustDirection}
Trust Type: {trustType}\n
"""
    
            values.append(result)
            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for v in values:
                    f.write(v + "\n")
            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
