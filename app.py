from datetime import timedelta

from flask import Flask, make_response
from flask_cors import CORS

from src.configuration.ConfigServer import ConfigServer
from src.routes.Casa import rutas_casa
from src.routes.Miembro import rutas_miembro
from src.routes.Solicitud import rutas_solicitud

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.register_blueprint(rutas_solicitud)
app.register_blueprint(rutas_miembro)
app.register_blueprint(rutas_casa)

config_server = ConfigServer("sharedz")
valores_config = config_server.patch(["crypt_password", "token_ttl"]).json()

app.config["SECRET_KEY"] = valores_config["crypt_password"]
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=valores_config["token_ttl"])
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = False


@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["OPTIONS"])
def prefligth(path):
	response = make_response()
	response.headers.add("Access-Control-Allow-Origin", "*")
	response.headers.add('Access-Control-Allow-Headers', "*")
	response.headers.add('Access-Control-Allow-Methods', "*")
	return response


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=42071, ssl_context=("cert.crt", "key.key"))
