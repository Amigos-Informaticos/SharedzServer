import json

from flask import Blueprint, Response, request

from src.model.Adoptante import Adoptante
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_ACCEPTABLE, NOT_FOUND, NO_CONTENT, OK, RESOURCE_CREATED
from src.util.Util import incluidos

rutas_solicitud = Blueprint("rutas_solicitud", __name__)


@rutas_solicitud.get("/solicitudes")
def obtener_solicitudes():
	respuesta = Response(status=NO_CONTENT)
	solicitudes = Adoptante.obtener_todas_solicitudes()
	if solicitudes:
		respuesta = Response(
			json.dumps(solicitudes),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_solicitud.get("/solicitudes/<id_adoptante>")
@Auth.requires_token
def obtener_solicitudes_adoptante(id_adoptante):
	respuesta = Response(status=NOT_FOUND)
	adoptante = Adoptante()
	adoptante.id_adoptante = id_adoptante
	if adoptante.cargar_adoptante():
		respuesta = Response(status=NO_CONTENT)
		solicitudes = adoptante.obtener_solicitudes()
		if solicitudes:
			respuesta = Response(
				json.dumps(solicitudes),
				status=OK,
				mimetype="application/json"
			)
	return respuesta


@rutas_solicitud.post("/solicitudes")
@Auth.requires_token
def solicitar_adopcion():
	respuesta = Response(status=NOT_ACCEPTABLE)
	requeridos = {"id_persona", "id_mascota"}
	payload = request.json
	if incluidos(requeridos, payload):
		adoptante = Adoptante()
		adoptante.id_adoptante = payload["id_persona"]
		estado, id_solicitud = adoptante.solicitar_adopcion(payload["id_mascota"])
		respuesta = Response(status=estado)
		if estado == RESOURCE_CREATED:
			solicitud = {
				"id_solicitud": id_solicitud,
				"id_persona": payload["id_persona"],
				"id_mascota": payload["id_mascota"],
				"estado": "Pendiente"
			}
			respuesta = Response(
				json.dumps(solicitud),
				status=estado,
				mimetype="application/json"
			)
	return respuesta


@rutas_solicitud.delete("/solicitudes/<id_adoptante>/<id_mascota>")
@Auth.requires_token
def eliminar_solicitud(id_adoptante, id_mascota):
	respuesta = Response(status=NOT_FOUND)
	adoptante = Adoptante()
	adoptante.id_adoptante = id_adoptante
	if adoptante.cargar_adoptante():
		respuesta = Response(status=adoptante.eliminar_solicitud(id_mascota))
	return respuesta
