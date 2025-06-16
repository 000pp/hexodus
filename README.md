<p align="center">
    <picture>
        <img src="img/logo_background_white.png">
    </picture>
</p>

<hr/>

Hexodus is a Python framework designed to enumerate Active Directory objects and assist with attacks using Windows protocols such as SMB, LDAP, RPC, and others. It uses an SQLite database to store collected data and a Flask-based web interface to make it easier to analyze the environment.

<br>

## Documentation
In the [documentation](https://github.com/000pp/hexodus/wiki), you can find guidance on how to use Hexodus commands, information on known errors reported by the community or by the developers, and possible solutions to those issues.

<br>

## Installation
We recommend using [pipx](https://github.com/pypa/pipx) to install the project, so you can run it from anywhere and make things easier.

### Linux
```
sudo apt install pipx git
pipx ensurepath
pix install git+https://github.com/000pp/hexodus
```

### MacOS
```
brew install pipx
pipx ensurepath
pix install git+https://github.com/000pp/hexodus
```

### Local
```
git clone https://github.com/000pp/hexodus.git
pipx install .
```

### Updating
```
pipx reinstall hexodus
```

<br>

## Usage

To start using Hexodus, you need to create a profile and configure the necessary information for LDAP and SMB binding. The basic usage is as follows:

1. Create a profile
```
hexodus -c <profile-name> <domain> <user> <password>
hexodus -c corp corp.local john.doe 'NewPassword123!'
```

2. Test the connection or run a module
```
hexodus corp ldap 192.168.15.52
hexodus corp ldap 192.168.15.52 users
hexodus corp smb  192.168.52.52 share
```

You can also list the available modules for each protocol by using `list` in place of the host argument:
```
hexodus corp ldap list
```

<br>

![image](https://github.com/user-attachments/assets/8120f17c-3d78-46ae-b783-37cdcc4cb78e)

![image](https://github.com/user-attachments/assets/004adcf6-1023-4313-acbb-abbf0eb4ff40)

![image](https://github.com/user-attachments/assets/98d6d1ba-0e4c-402c-b320-c228aa3a839a)

<br>

## To-Do
- [ ] Add interactive smb client 
- [ ] Add modules that uses WinRM protocol 
- [ ] Add vulnerabilities modules (BadSucessor, Backup Operator and other)
- [ ] Add module to download/read files remotely
- [ ] Add support to IP networks and files as input
- [ ] Add support to Kerberos
- [ ] Improve webview HTML and CSS
- [ ] Improve LDAP binding method
- [ ] Search for new protocols to use
- [ ] Automatize known-attacks (UnPAC the hash for example)

<br>

## Credits
- [NetExec](https://github.com/Pennyw0rth/NetExec)
- [Impacket](https://github.com/fortra/impacket)
- [SecTools](https://github.com/p0dalirius/sectools)
