from app import db
from datetime import datetime


class ResourceMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):

        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):

        db.session.delete(self)
        return db.session.commit()

    # def __str__(self):
    #     obj_id = hex(id(self))
    #     columns = self.__table__c.keys()

    #     values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
    #     return '<%s %s (%s)' % (obj_id, self.__class__.__name__, values)



