class About:
    license = 'MIT'
    name = 'Flask-Authlib'
    author = 'Abduaziz Ziyodov'
    version_info = ('1', '4', '0')
    version = '.'.join(version_info)
    author_email = 'abduaziz.ziyodov@mail.ru'
    copyright = '(c) 2021 by Abduaziz Ziyodov'
    url = 'https://github.com/AbduazizZiyodov/flask-authlib'
    description = 'Authentication library for Flask Web Framework '

    requires = [
        "flask", "flask_login", "psycopg2-binary",
        "sqlalchemy", "flask_sqlalchemy", "flask_bcrypt",
        "cryptography==3.3.2", "python-jose", "jwt",
        "pydantic", "email-validator", "gunicorn"
    ]

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Web Environment"
    ]
