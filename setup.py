from setuptools import setup, find_packages

setup(
    name="your-web-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
    Flask==2.2.3,
    Flask-Cors==4.0.0,
    Flask-HTTPAuth==4.8.0,
    Flask-Login==0.6.2,
    Flask-RESTful==0.3.10,
    Flask-WTF==1.1.1,
    gunicorn==21.2.0,
    Jinja2==3.1.2,
    multidict==6.0.4,
    Pillow==9.3.0,
    requests==2.31.0,
    requests-toolbelt==1.0.0,
    SQLAlchemy==2.0.7,
    SQLAlchemy-serializer==1.4.1,
    tzlocal==5.3.1,
    unicorn==2.0.1.post1,
    urllib3==2.2.1,
    Werkzeug==2.2.3,
    WTForms==3.0.1,
    ]
)
