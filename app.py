from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from src.configuration.ConfigServer import ConfigServer
from src.routes.Adoptante import rutas_adoptante

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.register_blueprint(rutas_adoptante)

config_server = ConfigServer("petMe")
valores_config = config_server.patch(["crypt_password", "token_ttl"]).json()

app.config["SECRET_KEY"] = valores_config["crypt_password"]
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=valores_config["token_ttl"])
app.config["SESSION_COOKIE_SECURE"] = True


@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	app.run()
