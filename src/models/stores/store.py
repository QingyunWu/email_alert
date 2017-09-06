import uuid
from src.common.database import Database
import src.models.stores.errors as StoreErrors
from urlparse import urlparse

__author__ = 'Qingyun Wu'


class Store(object):
	def __init__(self, name, url_prefix, tag_name, query, _id=None):
		self.name = name
		self.url_prefix = url_prefix
		self.tag_name = tag_name
		self.query = query
		self._id = uuid.uuid4().hex if _id is None else _id

	def __repr__(self):
		return "<Store {}>".format(self.name)

	def json(self):
		return {
			"_id": self._id,
			"name": self.name,
			"url_prefix": self.url_prefix,
			"tag_name": self.tag_name,
			"query": self.query
		}

	def delete(self):
		Database.remove("stores", {'_id': self._id})

	@classmethod
	def get_all_stores(cls):
		return [cls(**elem) for elem in Database.find("stores", {})]

	@classmethod
	def get_by_id(cls, id):
		return cls(**Database.find_one("stores", {"_id": id}))

	def save_to_mongo(self):
		Database.update("stores", {'_id': self._id}, self.json())

	@classmethod
	def get_by_name(cls, store_name):
		return cls(**Database.find_one("stores", {"name": store_name}))


	# from a www.amazon.com domain url to get a store
	@classmethod
	def get_store_by_domain_name(cls, url_prefix):
		return cls(**Database.find_one("stores", {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

	# employ urlparse to get the domain url of the item, parse it to the func get_by_url_prefix
	@classmethod
	def get_store_by_long_url(cls, url):
		str = urlparse(url)
		# get the www.amazon.com
		domain_url = str.netloc
		try:
			store = cls.get_store_by_domain_name(domain_url)
			return store
		except:
			raise StoreErrors.StoreNotFoundException("The item url didn't match any store!")
