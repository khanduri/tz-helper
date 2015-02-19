import application
import application.compute.services


##########################################
# GET RID OF THE FOLLOWING
##########################################


def compute_desc():
    return "basic"


def compute(a, b):
    application.compute.services.create_new_compute(a, b)
    return "a: %s + b: %s = %s" % (a, b, (a + b))
