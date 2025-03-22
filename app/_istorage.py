# -*- coding: utf-8 -*-
#
"""
Declares the abstract Storage interface class
"""

from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def load_items(self):
        """
        Returns a dictionary of dictionaries that
        contains the items information in the database.
        """
        pass

    @abstractmethod
    def add_item(self, *args, **kwargs):
        """
        Adds a movie to the items database.
        """
        pass

    @abstractmethod
    def delete_item(self, *args, **kwargs):
        """
        Deletes a movie from the items database.
        """
        pass

    @abstractmethod
    def update_item(self, *args, **kwargs):
        """
        Updates a movie from the items database.
        """
        pass


# - eof -
