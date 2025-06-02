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
![image](https://github.com/user-attachments/assets/8120f17c-3d78-46ae-b783-37cdcc4cb78e)

![image](https://github.com/user-attachments/assets/9f04bcbe-179d-4742-8103-806071d08f90)

![image](https://github.com/user-attachments/assets/98d6d1ba-0e4c-402c-b320-c228aa3a839a)

<br>

## To-Do
- [] Add interactive smb client 
- [] Add modules that uses WinRM protocol 
- [] Add vulnerabilities modules (BadSucessor, Backup Operator and other)
- [] Add module to download/read files remotely
- [] Improve webview HTML and CSS

<br>

## Credits
- [NetExec](https://github.com/Pennyw0rth/NetExec)
- [Impacket](https://github.com/fortra/impacket)
- [SecTools](https://github.com/p0dalirius/sectools)
