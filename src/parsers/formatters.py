from struct import unpack_from
from Cryptodome.Hash import MD4
from binascii import hexlify

from parsers.gmsa import MSDS_MANAGEDPASSWORD_BLOB

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
        
def fmt_sid(sid):
    """ Convert the SID binary to a readable string """

    revision, sub_authority_count = unpack_from("BB", sid, 0)
    identifier_authority = unpack_from(">Q", b"\x00\x00" + sid[2:8])[0]
    sub_authorities = unpack_from(f"<{sub_authority_count}I", sid, 8)

    sid_string = f"S-{revision}-{identifier_authority}"
    for sub_authority in sub_authorities:
        sid_string += f"-{sub_authority}"

    return sid_string

def fmt_gmsa(password):
    """ Transform GMSA blob password to usable NT hash """

    blob = MSDS_MANAGEDPASSWORD_BLOB()

    if len(password) != 0:
        blob.fromString(password)
        hash = MD4.new()
        hash.update(blob['CurrentPassword'][:-2])
        msDS_ManagedPassword_cleartext = hexlify(hash.digest()).decode("ascii")
        return msDS_ManagedPassword_cleartext
    
    return "None"