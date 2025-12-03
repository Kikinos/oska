import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
app.config['APP_NAME'] = "Business Management Portal"
app.config['APP_ICON'] = "fa-building"
app.config['APP_THEME'] = "bootstrap"

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

from . import models, views  # noqa
