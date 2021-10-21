import json

from flask import Blueprint, Response, request

from src.model.Mascota import Mascota
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_FOUND, OK

rutas_mascota = Blueprint("rutas_mascota", __name__)


@rutas_mascota.get("/mascotas/<id_mascota>")
@Auth.requires_token
def obtener_mascota(id_mascota):
	respuesta = Response(status=NOT_FOUND)
	solicitados = request.json
	mascota = Mascota()
	mascota.id_mascota = id_mascota
	if mascota.cargar():
		respuesta = Response(
			json.dumps(mascota.jsonificar(solicitados)),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_mascota.post("/mascotas/<id_mascota>")
@Auth.requires_token
def actualizar_mascota(id_mascota):
	respuesta = Response(status=NOT_FOUND)
	nuevos_valores = request.json
	mascota = Mascota()
	mascota.id_mascota = id_mascota
	if mascota.cargar():
		mascota.cargar_de_json(nuevos_valores)
		respuesta = Response(
			json.dumps(mascota.jsonificar()),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_mascota.delete("/mascotas/<id_mascota>")
@Auth.requires_token
def eliminar_mascota(id_mascota):
	mascota = Mascota()
	mascota.id_mascota = id_mascota
	return Response(status=mascota.eliminar())
