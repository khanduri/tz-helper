import application
import application.settings
import flask
import authomatic.adapters
import authomatic


auth = authomatic.Authomatic(application.settings.CONFIG, 'SUPER SEEKRIT SHTRINGG', report_errors=False)


@application.app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """

    # We need response object for the WerkzeugAdapter.
    response = flask.make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = auth.login(authomatic.adapters.WerkzeugAdapter(flask.request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()

        # The rest happens inside the template.
        return flask.render_template('index.html', result=result)

    # Don't forget to return the response.
    return response
