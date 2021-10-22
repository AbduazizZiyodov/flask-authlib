# 🏡 Home Page


<h1 align="center"><b>Flask-Authlib 🔐</b></h1>

<p align="center">
    <img src="https://badge.fury.io/py/Flask-Authlib.svg">
    <img src="https://static.pepy.tech/personalized-badge/flask-authlib?period=total&units=none&left_color=blue&right_color=green&left_text=Downloads">
</p>

<p align="center">
    Welcome 👋
    <br>
    <b>Flask-Authlib</b> - Authentication Library For Flask Web Framework 🔥
</p>

<hr>

# Installation

Create virtual environment for your python project:

```bash
python -m venv env
```

!!! info "Virtual Environment"
    The `venv` module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories.

    **Python docs** - [Creation of virtual environments](https://docs.python.org/3/library/venv.html)

Activate it:

=== "Linux"
    `bash/zsh`:

    ``` bash
    $ ls
        env/
    $ source env/bin/activate
    ```

=== "Windows"
    `cmd.exe`:

    ```cmd
    C:\> env\Scripts\activate.bat
    ```
    `PowerShell`:

    ```powershell
    PS C:\> <venv>\Scripts\Activate.ps1
    ```
    !!! info "Note"
        On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:

        ```powershell
        PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        ```

        *From python docs*



Install this library by using `pip` command:

```bash
$ pip install -U flask_authlib
```

!!! info "Licence"
    This project is licensed under the terms of the MIT license.

```
$ pip show flask_authlib

Name: Flask-Authlib
Version: 1.4.0
Summary: Authentication library for Flask Web Framework    
Home-page: https://github.com/AbduazizZiyodov/flask-authlib
Author: Abduaziz Ziyodov
Author-email: abduaziz.ziyodov@mail.ru
License: MIT
Location: ...
Requires: ...

```