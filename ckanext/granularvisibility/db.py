import datetime
import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

#Schema of package_granular_visibility table
granular_visibility_mapping_table = Table('granular_visibility_mapping', metadata,
    Column('packageid', types.UnicodeText, primary_key=True),
    Column('visibilityid', types.UnicodeText)
)

#Commands that can be preformed on table
class granular_visibility_mapping(model.DomainObject):
    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def get_all(cls, **kw):
        query = model.Session.query(cls).all()
        return query

    @classmethod
    def find(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw)

model.meta.mapper(granular_visibility_mapping, granular_visibility_mapping_table)

#Schema of package_granular_visibility table
granular_visibility_table = Table('granular_visibility', metadata,
    Column('visibilityid', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('visibility', types.UnicodeText),
    Column('ckanmapping', types.BOOLEAN),
    Column('description', types.UnicodeText)
)

#Commands that can be preformed on table
class granular_visibility(model.DomainObject):
    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def get_all(cls, **kw):
        query = model.Session.query(cls).all()
        return query

    @classmethod
    def find(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw)

model.meta.mapper(granular_visibility, granular_visibility_table)