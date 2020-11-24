# OnlineClassManager

This is a demo application that includes features for online class managing such as real-time poll and attendance monitoring built using [Python](https://www.python.org/) and [Flask](http://flask.pocoo.org/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software.

* Git.
* Python.
* Pip.

## Install

Clone the git repository on your computer

> $ git clone https://github.com/AjayKini2000/OnlineClassManager.git

You can also download the entire repository as a zip file and unpack in on your computer if you do not have git

After cloning the application, you need to install it's dependencies.

> $ cd OnlineClassManager

> $ pip install flask
> $ pip install requests
> $ pip install flask-sqlalchemy
> $ pip install flask-login

## Setup

* In a terminal, you can set the FLASK_APP and FLASK_DEBUG values(For Windows replace export with set):
> $ export FLASK_APP=project
> $ export FLASK_DEBUG=1

## Run the application
 
> $ flask run

> Open a web browser and open the URL displayed in the command line to see the Home page. e.g. http://127.0.0.1:5000/

## Built With

* [Python](https://www.python.org/) - a programming language that lets you work quickly and integrate systems more effectively
* [Flask](http://flask.pocoo.org/) - a microframework for Python based on Werkzeug, Jinja 2 and good intentions
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - library for session management
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - to create a user model
