import json

from flask import Blueprint, Response, request, session

from src.model.Miembro import Miembro
from src.routes.Auth import Auth
from src.routes.HTTPStatus import OK, RESOURCE_CREATED

rutas_miembro = Blueprint("rutas_miembro", __name__)


@rutas_miembro.post("/login")
@Auth.requires_payload({"email", "password"})
def login():
	payload = request.json
	miembro = Miembro()
	miembro.email = payload["email"]
	miembro.set_password(payload["password"])
	estado = miembro.login()
	respuesta = Response(status=estado)
	if estado == OK:
		if miembro.cargar():
			token = Auth.generate_token(miembro)
			session.permanent = True
			session["token"] = token
			session["email"] = miembro.email
			session["password"] = miembro.password
			respuesta = Response(
				json.dumps({
					"token": token,
					"id": miembro.id_miembro
				}),
				status=estado,
				mimetype="application/json"
			)
	return respuesta


@rutas_miembro.post("/miembros")
@Auth.requires_payload({"nombre", "email", "password"})
def registrar():
	payload = request.json
	miembro = Miembro()
	miembro.cargar_de_json(payload)
	estado = miembro.registrar()
	respuesta = Response(status=estado)
	if estado == RESOURCE_CREATED:
		respuesta = Response(
			json.dumps(miembro.jsonificar()),
			status=estado,
			mimetype="application/json"
		)
	return respuesta
