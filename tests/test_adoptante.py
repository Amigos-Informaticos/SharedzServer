from src.model.Adoptante import Adoptante
from src.routes.HTTPStatus import CONFLICT, OK, RESOURCE_CREATED

adoptante = Adoptante()
adoptante.nombre = "Miguel Joaquin"


def test_guardar():
	estado = adoptante.guardar()
	assert estado == RESOURCE_CREATED or CONFLICT


def test_actualizar():
	adoptante.email = "correo@correo.com"
	adoptante.cargar_adoptante()
	adoptante.set_password("contraChida")
	assert adoptante.actualizar() == True


def test_login():
	adoptante.email = "correo@correo.com"
	adoptante.set_password("contraChida")
	assert adoptante.login() == OK


def test_cargar():
	adoptante.email = "correo@correo.com"
	cargado = adoptante.cargar_adoptante()
	assert cargado == True


def test_eliminar():
	assert adoptante.eliminar() == True
