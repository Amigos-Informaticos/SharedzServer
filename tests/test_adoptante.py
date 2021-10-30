import pytest

from src.model.Adoptante import Adoptante
from src.routes.HTTPStatus import OK, RESOURCE_CREATED

adoptante = Adoptante()
adoptante.nombre = "Miguel Joaquin"


def test_guardar():
	assert adoptante.guardar() == RESOURCE_CREATED


def test_actualizar():
	assert adoptante.id_adoptante is not None
	adoptante.cargar_adoptante()
	adoptante.email = "correo@correo.com"
	adoptante.set_password("contraChida")
	assert adoptante.actualizar() == OK


@pytest.mark.dependency()
def test_login():
	adoptante.email = "correo@correo.com"
	adoptante.set_password("contraChida")
	assert adoptante.login() == OK


@pytest.mark.dependency(depends=["test_login"])
def test_cargar():
	adoptante.email = "correo@correo.com"
	cargado = adoptante.cargar_adoptante()
	assert cargado == True


@pytest.mark.dependency(depends=["test_login"])
def test_eliminar():
	assert adoptante.eliminar() == OK
