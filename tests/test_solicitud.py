import pytest

from src.model.Adoptante import Adoptante
from src.model.Mascota import Mascota
from src.routes.HTTPStatus import OK, RESOURCE_CREATED

adoptante = Adoptante()
adoptante.nombre = "Adoptante de Prueba"

mascota = Mascota()
mascota.nombre = "Mauricio"


@pytest.mark.dependency()
def test_registrar_adoptante():
	assert adoptante.guardar() == RESOURCE_CREATED


@pytest.mark.dependency()
def test_registrar_mascota():
	assert mascota.guardar() == RESOURCE_CREATED


@pytest.mark.dependency(depends=["test_registrar_adoptante", "test_registrar_mascota"])
def test_solicitar_adopcion():
	estado, _ = adoptante.solicitar_adopcion(mascota.id_mascota)
	assert estado == RESOURCE_CREATED


@pytest.mark.dependency(depends=["test_registrar_adoptante"])
def test_eliminar_adoptante():
	assert adoptante.eliminar() == OK


@pytest.mark.dependency(depends=["test_registrar_mascota"])
def test_eliminar_mascota():
	assert mascota.eliminar() == OK
