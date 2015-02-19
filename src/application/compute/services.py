import application.compute.models


##########################################
# Collection operations
##########################################


def fetch_all_computes():
    computes = application.compute.models.ComputeQuery.select_all()
    return computes


def create_new_compute(a, b):
    compute = application.compute.models.ComputeQuery.insert_single(a, b)
    return compute


def remove_all_computes():
    application.compute.models.ComputeQuery.delete_all()
    return True


##########################################
# Resource operations
##########################################


def fetch_compute(compute_id):
    compute = application.compute.models.ComputeQuery.select_by_id(compute_id)
    return compute


def modify_compute(compute_id, a, b):
    compute = application.compute.models.ComputeQuery.update_by_id(compute_id, a, b)
    return compute


def remove_compute(compute_id):
    application.compute.models.ComputeQuery.delete_by_id(compute_id)
    return True
