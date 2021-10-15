import json

from flask import Blueprint, Response, request

from src.model.Refugio import Refugio
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_ACCEPTABLE, NOT_FOUND, OK, RESOURCE_CREATED

rutas_refugio = Blueprint("rutas_refugio", __name__)


@rutas_refugio.post("/refugios")
@Auth.requires_token
def registrar():
	respuesta = Response(status=NOT_ACCEPTABLE)
	vals = request.json
	if "nombre" in vals:
		refugio = Refugio()
		refugio.cargar_de_json(vals)
		estado = refugio.guardar()
		respuesta = Response(status=estado)
		if estado == RESOURCE_CREATED:
			respuesta = Response(
				json.dumps(refugio.jsonificar()),
				status=estado,
				mimetype="application/json"
			)
	return respuesta


@rutas_refugio.get("/refugios/<id_refugio>")
@Auth.requires_token
def obtener(id_refugio):
	respuesta = Response(status=NOT_FOUND)
	refugio = Refugio()
	refugio.id_refugio = id_refugio
	solicitados = request.json
	if refugio.cargar():
		respuesta = Response(
			json.dumps(refugio.jsonificar(solicitados)),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_refugio.post("/refugios/<id_refugio>")
@Auth.requires_token
def actualizar(id_refugio):
	respuesta = Response(status=NOT_FOUND)
	nuevos_valores = request.json
	refugio = Refugio()
	refugio.id_refugio = id_refugio
	refugio.cargar_de_json(nuevos_valores)
	estado = refugio.actualizar()
	if estado == OK:
		refugio.cargar()
		respuesta = Response(
			json.dumps(refugio.jsonificar()),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_refugio.delete("/refugios/<id_refugio>")
@Auth.requires_token
def eliminar(id_refugio):
	respuesta = Response(status=NOT_FOUND)
	refugio = Refugio()
	refugio.id_refugio = id_refugio
	respuesta = Response(status=refugio.eliminar())
	return respuesta
