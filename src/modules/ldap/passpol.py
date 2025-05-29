from rich.console import Console
console = Console()
from uuid import uuid4

class Passpol:
    name = "passpol"
    desc = "Get the domain password policy"
    search_filter = "(objectClass=domainDNS)"
    attributes = ["lockoutDuration", "lockoutThreshold", "maxPwdAge", "minPwdAge", "minPwdLength"]

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
            lockoutDuration = entry.lockoutDuration.value or "None"
            lockoutThreshold = f"{entry.lockoutThreshold.value} - Password Spray is possible!" if entry.lockoutThreshold.value == 0 else entry.lockoutThreshold.value or "None"
            maxPwdAge = entry.maxPwdAge.value or "None"
            minPwdAge = entry.minPwdAge.value or "None"
            minPwdLength = entry.minPwdLength.value or "None"

            result = f"""Lockout Duration: {lockoutDuration}
Lockout Threshold: {lockoutThreshold}
Max Password Age: {maxPwdAge}
Min Password Age: {minPwdAge}
Min Password Length: {minPwdLength}"""
            values.append(result)

            console.print(result, highlight=False)

        if save_output:
            filename = f"{self.name}_{uuid4().hex}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                for value in values:
                    file.write(value)

            console.print(f"\n[[green]+[/]] Output saved to {filename}", highlight=False)

        return values
