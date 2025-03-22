# -*- coding: utf-8 -*-
#
"""
Implements JsonStorage-class for CRUD-operations on a
JSON file that contains information about generic items.
"""

from os import path
from collections import defaultdict
from msgspec import json
from _istorage import IStorage


class JsonStorage(IStorage):
    """
    Implements CRUD-Operations on a JSON file that contains
    information about generic items.
    """

    def __init__(self, file_path: str):
        """
        Assert the existence of a storage in a JSON file at 'file_path'.
        """
        if len(file_path) < 1:
            raise ValueError("argument 'file_path' is an empty string")
        if not path.exists(file_path):
            raise IOError(f"ENOENT: '{file_path}' does not exist.")
        self._path = file_path

    def load_items(self) -> list[dict]:
        """
        Returns a list of dictionaries that
        contains the information about items in the database.
        """
        items: list[dict]
        with open(self._path, "r", encoding="utf-8") as fp:
            items = json.decode(fp.read(), type=list[dict])
        return items

    def _commit(self, *args, **kwargs):
        """
        Saves the <items> data to a JSON database.
        """
        json_data = json.encode(kwargs["items"])
        with open(self._path, "wb") as fp:
            fp.write(json_data)

    def add_item(self, /, item: dict = {}, *args, **kwargs):
        """
        Adds a dictionary item to the database.
        """
        items: list[dict] = self.load_items()
        if not item:
            for key, value in kwargs.items():
                item[key] = value
        items.append(item)
        self._commit(items=items)

    def get_new_item(self) -> dict:
        """
        Gets a new item with an unique 'id'-key initialized.
        """
        new_item: dict = defaultdict(int)
        items: list[dict] = self.load_items()
        for item in items:
            new_item["id"] = max(new_item["id"], item["id"])
        new_item["id"] += 1
        return new_item

    def get_item(self, id: int, /, *args, **kwargs) -> dict | None:
        """
        Gets an item with <id> from the items-database.
        May return None, if item was not found.
        """
        items: list[dict] = self.load_items()
        try:
            index = self._index_of_item(id, items)
            return items[index]
        except IndexError as e:
            print(f"{e.message}")
            return None

    def delete_item(self, id: int, /, *args, **kwargs):
        """
        Deletes an item with <id> from the items-database.
        """
        items: list[dict] = self.load_items()
        index = self._index_of_item(id, items)
        items.pop(index)
        self._commit(items=items)

    def update_item(self, id: int, /, *args, **kwargs):
        """
        Updates an item with <id> with given key-value pairs
        of **kwargs in the items database.
        """
        items: list[dict] = self.load_items()
        index = self._index_of_item(id, items)
        items[index].update(**kwargs)
        self._commit(items=items)

    def _index_of_item(self, id: int, items: list[dict]) -> int:
        """
        Looks up a list of dictionaries, if it includes the
        key 'id' with value of the argument 'id' given.
        Returns the index of 'id' in 'items'.
        Raises an exception of kind IndexError, if not found.
        """
        for item in enumerate(items):
            if id == item[1]["id"]:
                return item[0]
        raise IndexError(f"ENOENT: an item with id '{id}' does not exist.")
