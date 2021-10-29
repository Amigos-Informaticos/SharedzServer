from flask import Blueprint

from src.routes.Auth import Auth

rutas_solicitud = Blueprint("rutas_solicitud", __name__)

@rutas_solicitud.post("/solicitudes")
@Auth.requires_token
def solicitar_adopcion():
	respuesta
	requeridos = {"id_persona", "id_mascota"}
