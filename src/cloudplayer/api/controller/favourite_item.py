"""
    cloudplayer.api.controller.favourite_item
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by Nicolas Drebenstedt
    :license: GPL-3.0, see LICENSE for details
"""
from cloudplayer.api.controller import Controller
from cloudplayer.api.model.favourite_item import FavouriteItem


class FavouriteItemController(Controller):

    __model__ = FavouriteItem