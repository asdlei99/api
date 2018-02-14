"""
    cloudplayer.api.base.model
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by Nicolas Drebenstedt
    :license: GPL-3.0, see LICENSE for details
"""
import datetime
import json

import sqlalchemy as sql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from cloudplayer.api.access import Deny, Fields


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Model(object):

    __acl__ = (Deny(),)
    __fields__ = Fields()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created = sql.Column(
        sql.DateTime, server_default=utcnow())
    updated = sql.Column(
        sql.DateTime, server_default=utcnow(), onupdate=utcnow())

    account_id = None
    provider_id = None
    parent = None

    @property
    def account(self):
        # XXX: Check session for this account id without querying
        from cloudplayer.api.model.account import Account
        return Account(id=self.account_id, provider_id=self.provider_id)


Base = declarative_base(cls=Model)


class Encoder(json.JSONEncoder):

    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:  # NOQA
            if isinstance(obj, Base):
                dict_ = {c: getattr(obj, c) for c in obj.__fields__}
                if dict_.get('id'):  # TODO: There must be a better solution
                    dict_['id'] = str(dict_['id'])
                return dict_
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            elif isinstance(obj, datetime.timedelta):
                return obj.total_seconds()
            return json.JSONEncoder.default(self, obj)
