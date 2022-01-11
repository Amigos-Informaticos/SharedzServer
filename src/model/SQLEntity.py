from src.connection.EasyConnection import EasyConnection


class SQLEntity:
	def __init__(self):
		self.connection = EasyConnection.build_from_static()
		self.ignored_attributes = ["ignored_attributes", "connection"]

	def ignore_attribute(self, attribute_name: str) -> bool:
		ignored: bool = False
		if attribute_name in self.__dict__:
			self.ignored_attributes.append(attribute_name)
			ignored = True
		return ignored

	def remove_ignored(self, attribute_name: str) -> bool:
		removed: bool = False
		if attribute_name in self.__dict__ and attribute_name in self.ignored_attributes:
			self.ignored_attributes.remove(attribute_name)
			removed = True
		return removed

	def watched_attributes(self) -> list:
		watched_attributes: list = []
		for attribute in self.__dict__:
			if attribute not in self.ignored_attributes:
				watched_attributes.append(attribute)
		return watched_attributes
