import pytest

from src.model.Mascota import Mascota
from src.routes.HTTPStatus import OK, RESOURCE_CREATED

mascota = Mascota()
mascota.nombre = "Mauricio"


@pytest.mark.dependency()
def test_guardar():
	assert mascota.guardar() == RESOURCE_CREATED


@pytest.mark.dependency(depends=["test_guardar"])
def test_actualizar():
	assert mascota.id_mascota is not None
	mascota.peso = 2
	mascota.color = "Rojecito"
	assert mascota.actualizar() == OK


@pytest.mark.dependency(depends=["test_guardar"])
def test_cargar():
	assert mascota.cargar() == True
	print(mascota.__dict__)


@pytest.mark.dependency(depends=["test_guardar"])
def test_eliminar():
	assert mascota.eliminar() == OK
