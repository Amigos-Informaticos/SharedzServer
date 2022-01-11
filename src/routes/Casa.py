import json

from flask import Blueprint, Response, request

from src.model.Casa import Casa
from src.model.Miembro import Miembro
from src.routes.Auth import Auth
from src.routes.HTTPStatus import INTERNAL_SERVER_ERROR, RESOURCE_CREATED

rutas_casa = Blueprint("rutas_casa", __name__)


@rutas_casa.post("/casas")
@Auth.requires_payload({"nombre", "id_creador"})
@Auth.requires_token
def registrar_casa():
	payload = request.json
	miembro_creador = Miembro()
	miembro_creador.id_miembro = payload["id_creador"]
	miembro_creador.cargar()

	nueva_casa = Casa()
	nueva_casa.nombre = payload["nombre"]
	respuesta = Response(status=INTERNAL_SERVER_ERROR)
	if nueva_casa.registrar(miembro_creador):
		nueva_casa.cargar_miembros()
		respuesta = Response(
			json.dumps(nueva_casa.jsonificar()),
			status=RESOURCE_CREATED,
			mimetype="application/json"
		)
	return respuesta
