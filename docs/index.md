# **Welcome 👋**

<h1 align="center"><b>Flask-Authlib 🔐</b></h1>

<p align="center">
    <img src="https://badge.fury.io/py/Flask-Authlib.svg">
    <img src="https://static.pepy.tech/personalized-badge/flask-authlib?period=total&units=none&left_color=blue&right_color=green&left_text=Downloads">
</p>

<p align="center">
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

=== "Bash/zsh"

    ``` bash
    $ source env/bin/activate
    ```

=== "Cmd"

    ```cmd
    C:\> env\Scripts\activate.bat
    ```

=== "Powershell"

    ```powershell
    PS C:\> <venv>\Scripts\Activate.ps1
    ```

    !!! info "Note"

        On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:

        ```powershell
        PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        ```

        *From python docs*

=== "Git Bash"

    ```bash
    $ source env/Scripts/activate
    ```

<hr>

Install this library by using `pip` command:

```bash
$ pip install -U flask_authlib
```

```
$ pip show flask_authlib

Name: Flask-Authlib
Version: 1.5.0
Summary: Authentication library for Flask Web Framework
Home-page: https://github.com/AbduazizZiyodov/flask-authlib
Author: Abduaziz Ziyodov
Author-email: abduaziz.ziyodov@mail.ru
License: MIT
Location: ...
Requires: ...

```

# **✨ Features**

!!! success "Goal of Project"

    To allow python developers to add authentication functionality with one line of code!

- [x] Library adds built-in `frontend` and `backend` that implements authentication functionality to your flask application automatically.

- [x] The login and registration pages are ready for use. After starting and initializing your flask application templates (`templates/`) and static (`static/`) files will be copied on your app's folder (if you want, you can change these files any time).

- [x] Better customization! You can customize this library by its configs. There are three types of configs:
  - **Base** config
  - **Templates** config
  - **Alerts** config (alert messages)

!!! help "Flask For Beginners"

    If you are a beginner in flask development, you can learn the basics of the flask on the `Flask For Beginners` section 🙂