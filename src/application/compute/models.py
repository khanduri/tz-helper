import application.compute.data.google_data_store


class ComputeModel(object):

    def __init__(self, data):
        self.data = data
        for k, v in data.iteritems():
            setattr(self, k, v)


ComputeQuery = application.compute.data.google_data_store.ComputeQuery(ComputeModel)
