import uuid
from bs4 import BeautifulSoup
import requests
import re
from flask import url_for

from flask import make_response
from werkzeug.utils import redirect

from src.common.database import Database
from src.models.stores.store import Store
import src.models.stores.errors as StoreErrors
__author__ = 'Qingyun Wu'


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        try:
            store = Store.get_store_by_long_url(url)
        except StoreErrors.StoreException as e:
            return redirect(url_for('home'))
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # query is a dict, for Amazon, tag is span, query is{id="sss", class="ssdafd"}
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
		# extract only the price number
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())

        return self.price

    def save_to_mongo(self):
        Database.update("items", {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one("items", {"_id": item_id}))
