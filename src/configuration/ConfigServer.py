import os

import requests
from requests import Response

from src.configuration.Configuration import Configuration


class ConfigServer:
	def __init__(self, client_name: str, config_path: str = None):
		if config_path is None:
			root = os.path.dirname(os.path.abspath(__file__))
			config_path = root + "/" + "connection.json"
		server_url = Configuration.get_from_json("config_server_url", config_path)
		self.path = server_url + "/" + client_name

	def get(self, key: str, parameters: list = []) -> Response:
		return requests.get(self.path + "/" + key, params=parameters)

	def post(self, payload: dict or list = [], parameters: list = []) -> Response:
		return requests.post(self.path, json=payload, params=parameters)

	def put(self, payload: dict or list = [], parameters: list = []) -> Response:
		return requests.put(self.path, json=payload, params=parameters)

	def patch(self, payload: dict or list = [], parameters: list = []) -> Response:
		return requests.patch(self.path, json=payload, params=parameters)

	def delete(self, payload: dict or list = [], parameters: list = []) -> Response:
		return requests.delete(self.path, json=payload, params=parameters)