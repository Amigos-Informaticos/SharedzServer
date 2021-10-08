import json

from flask import Blueprint, Response, request, session

from src.model.Adoptante import Adoptante
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_ACCEPTABLE, OK
from src.util.Util import incluidos

rutas_adoptante = Blueprint("rutas_adoptante", __name__)


@rutas_adoptante.route("/login", methods=["POST"])
def login():
	requeridos: set = {"email", "password"}
	respuesta = Response(status=NOT_ACCEPTABLE)
	valores_json = request.json
	if incluidos(requeridos, valores_json):
		adoptante = Adoptante()
		adoptante.email = valores_json["email"]
		adoptante.set_password(valores_json["password"])
		estado = adoptante.login()
		respuesta = Response(status=estado)
		if estado == OK:
			if adoptante.cargar_adoptante():
				token = Auth.generate_token(adoptante)
				session.permanent = True
				session["token"] = token
				session["email"] = adoptante.email
				session["password"] = adoptante.password
				respuesta = Response(
					json.dumps({
						"token": token,
						"id": adoptante.id_adoptante
					}),
					status=estado,
					mimetype="application/json"
				)
	return respuesta
