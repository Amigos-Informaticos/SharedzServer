import json
from typing import Any


class Configuration:
	@staticmethod
	def get_from_json(key: str, json_path: str = "src/configuration/connection.json") -> Any:
		value = None
		with open(json_path) as json_file:
			data = json.load(json_file)
			if key in data:
				value = data[key]
		return value

	@staticmethod
	def save_to_json(key: str, value: Any, json_path: str = "src/configuration/connection.json"):
		with open(json_path) as json_file:
			data = json.load(json_file)
		open(json_path, "w").close()
		data[key] = value
		with open(json_path, "w") as json_file:
			json.dump(data, json_file, indent=2)
