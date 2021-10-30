import json

from flask import Blueprint, Response, request

from src.model.Refugio import Refugio
from src.routes.Auth import Auth
from src.routes.HTTPStatus import NOT_ACCEPTABLE, NOT_FOUND, NO_CONTENT, OK, RESOURCE_CREATED

rutas_refugio = Blueprint("rutas_refugio", __name__)


@rutas_refugio.get("/refugios")
def obtener_refugios():
	respuesta = Response(status=NO_CONTENT)
	nombre = request.args.get("nombre", default=None, type=str)
	estado = request.args.get("estado", default=None, type=str)
	localidad = request.args.get("localidad", default=None, type=str)
	pagina = request.args.get("pagina", default=0, type=int)
	refugios = Refugio.buscar_refugios(nombre, estado, localidad, pagina)
	if refugios:
		url = "https://amigosinformaticos.ddns.net:42070/refugios?"
		if nombre is not None:
			url += f"nombre={nombre}&"
		if estado is not None:
			url += f"estado={estado}&"
		if localidad is not None:
			url += f"localidad={localidad}&"
		json_respuesta = {
			"refugios": refugios,
			"sig": url + f"pagina={pagina + 1}"
		}
		if pagina > 0:
			json_respuesta["prev"] = url + f"pagina={pagina - 1}"
		respuesta = Response(
			json.dumps(json_respuesta),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


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
	refugio.cargar()
	refugio.cargar_de_json(nuevos_valores)
	estado = refugio.actualizar()
	if estado == OK:
		respuesta = Response(
			json.dumps(refugio.jsonificar()),
			status=OK,
			mimetype="application/json"
		)
	return respuesta


@rutas_refugio.delete("/refugios/<id_refugio>")
@Auth.requires_token
def eliminar(id_refugio):
	refugio = Refugio()
	refugio.id_refugio = id_refugio
	return Response(status=refugio.eliminar())
