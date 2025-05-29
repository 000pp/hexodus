def fmt_multi(input):
    """ Format values that can be str, list or None and returns an formatted string """

    if isinstance(input, list) and input:
        return ", ".join(input)
    
    if isinstance(input, str) and input:
        return input
    
    return "None"

def fmt_uac(value):
    """ Get UAC value and format to understandable UAC status """

    uac_values = {
        "512": "User is Enabled - Password Expires",
        "514": "User is Disabled - Password Expires",
        "66048": "User is Enabled - Password Never Expires",
        "66050": "User is Disabled - Password Never Expires",
        "1114624": "User is Enabled - Password Never Expires - User Not Delegated",
        "1049088": "User is Enabled - Password Expires - User Not Delegated",
        "17891840": "User is Enabled - [bold yellow]Password Never Expires - [bold yellow]User Trusted to Delegate",
        "66176": "Password Never Expires - ms-DS-User-Encrypted-Text-Password-Allowed is true",
        "4096": "WORKSTATION_TRUST_ACCOUNT",
    }

    for uac_value, description in uac_values.items():
        if int(uac_value) == value:
            return description