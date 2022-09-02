import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import views

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        db_path = os.path.join(app.instance_path, "db.sqlite3")
        db_url = f"sqlite:///{db_path}"
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)
    #Adding routing for app
    #Endpoint below works for the get and post methods and handles optional parameters for the get request
    app.add_url_rule("/trades","trades",view_func = views.TradesAPI.as_view('trades'))
    #Endpoint below takes in a trade id as a parameter to return a specific trade
    app.add_url_rule("/trades/<id>","trades_id",view_func = views.TradesIDAPI.as_view('trades_id'))
    
    # Might not be needed, there is a discrepancy between the readme, 
    # the header of the hackerrank instructions and part 1 of hackerrank description
    # app.add_url_rule("/ret_settlement_dates","ret_settlement",view_func = views.RetSettlement.as_view('ret_settlement'))
    # app.add_url_rule("/agg_monthly","agg_monthly",view_func = views.AggMonthly.as_view('agg_monthly'))
    return app

def init_db():
    db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
