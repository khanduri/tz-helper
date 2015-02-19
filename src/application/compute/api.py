import application.base.decorators
import application.compute.forms
import application.compute.services


##########################################
# Collection operations
##########################################

@application.base.decorators.return_json
def get_all_computes():
    computes = application.compute.services.fetch_all_computes()
    compute_list = [e.data for e in computes]
    return 200, compute_list


@application.base.decorators.return_json
def post_compute():
    form = application.compute.forms.ComputeForm(csrf_enabled=False)
    if form.validate_on_submit():
        application.compute.services.create_new_compute(form.data.get('a'), form.data.get('b'))
        return 200, {}
    return 404, {}


@application.base.decorators.return_json
def delete_all_computes():
    application.compute.services.remove_all_computes()
    return 200, {}


##########################################
# Resource operations
##########################################


@application.base.decorators.return_json
def get_compute(compute_id):
    compute_instance = application.compute.services.fetch_compute(compute_id)
    return 200, compute_instance.data


@application.base.decorators.return_json
def update_compute(compute_id):
    form = application.compute.forms.ComputeForm(csrf_enabled=False)
    if form.validate_on_submit():
        compute_instance = application.compute.services.modify_compute(compute_id, form.data.get('a'), form.data.get('b'))
        return 200, compute_instance.data
    return 404, {}


@application.base.decorators.return_json
def delete_compute(compute_id):
    application.compute.services.remove_compute(compute_id)
    return 200, {}
