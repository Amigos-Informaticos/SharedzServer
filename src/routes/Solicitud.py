import json

from flask import Blueprint, Response, request

from src.model.Adoptante import Adoptante
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_ACCEPTABLE, RESOURCE_CREATED
from src.util.Util import incluidos

rutas_solicitud = Blueprint("rutas_solicitud", __name__)


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
