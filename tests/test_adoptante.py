from src.model.Adoptante import Adoptante
from src.routes.HTTPStatus import OK

adoptante = Adoptante()
adoptante.nombre = "Miguel Joaquin"


def test_guardar():
	assert adoptante.guardar() == True
	assert adoptante.id_adoptante is not None


def test_actualizar():
	adoptante.email = "correo@correo.com"
	adoptante.cargar_adoptante()
	adoptante.set_password("contraChida")
	assert adoptante.actualizar() == True


def test_login():
	assert adoptante.login() == OK


def test_cargar():
	adoptante.email = "correo@correo.com"
	cargado = adoptante.cargar_adoptante()
	print(adoptante.__dict__)
	assert cargado == True


def test_eliminar():
	assert adoptante.eliminar() == True
