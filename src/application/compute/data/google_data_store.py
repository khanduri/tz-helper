import google.appengine.ext.ndb


class Compute(google.appengine.ext.ndb.Model):

    a = google.appengine.ext.ndb.IntegerProperty(required=True)
    b = google.appengine.ext.ndb.IntegerProperty(required=True)

    timestamp_created = google.appengine.ext.ndb.DateTimeProperty(auto_now=True)
    timestamp_removed = google.appengine.ext.ndb.DateTimeProperty(auto_now=True)
    timestamp_modified = google.appengine.ext.ndb.DateTimeProperty(auto_now=True)

    def get_dict_repr(self):
        data = {
            'id': self.key.id(),
            'a': self.a,
            'b': self.b,
            'timestamp_created': self.timestamp_created,
            'timestamp_removed': self.timestamp_removed,
            'timestamp_modified': self.timestamp_modified,
        }
        return data


class ComputeQuery(object):

    def __init__(self, model_class):
        self.model_class = model_class

    ##########################################
    # Collection operations
    ##########################################

    def select_all(self):
        computes = Compute.query()
        return [self.model_class(c.get_dict_repr()) for c in computes]

    def insert_single(self, a, b):
        compute = Compute(a=a, b=b)
        compute.put()
        return self.model_class(compute.get_dict_repr())

    def delete_all(self):
        computes = Compute.query()
        list_of_keys = [c.key for c in computes]
        google.appengine.ext.ndb.delete_multi(list_of_keys)
        return True

    ##########################################
    # Resource operations
    ##########################################

    def select_by_id(self, compute_id):
        compute = Compute.get_by_id(compute_id)
        return self.model_class(compute.get_dict_repr())

    def update_by_id(self, compute_id, a, b):
        compute = Compute.get_by_id(compute_id)
        compute.a = a
        compute.b = b
        compute.put()
        return self.model_class(compute.get_dict_repr())

    def delete_by_id(self, compute_id):
        compute = Compute.get_by_id(compute_id)
        compute.key.delete()
        return True
