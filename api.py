import flask
from flask import jsonify, Response, send_from_directory, request
from apidoc import spec, ApiInfo, CorpusMetadata
from sparql import DB
import os
import json

service_version = "0.1.0"
"""SERVICE_VERSION: Version of the service.
"""

service_url = str(os.environ.get("SERVICE_URL", "http://localhost"))
"""SERVICE_URL: url where the service can be accessed.
Normally, it's somehow set when running the flask dev server
but it needs to be adapted, when one wants to access the docker container
default is "localhost".
"""

service_port = int(os.environ.get("SERVICE_PORT", 5000))
"""SERVICE_PORT: Port of the running service.
flask's default is 5000
"""

# Debug Mode: Activates the flask Debug Mode
if os.environ.get("SERVICE_DEBUG", "TRUE") == "FALSE":
    debug = False
else:
    debug = True

# Triple Store Connection Details are retrieved from environment variables

triplestore_name = str(os.environ.get("CONN_TRIPLESTORE", "virtuoso"))
"""CONN_TRIPLESTORE: Name of the Triple Store.
Default implementation is based on Virtuoso.
"""

triplestore_protocol = os.environ.get("CONN_PROTOCOL", "http")
"""CONN_PROTOCOL: Postdata's current implementation uses http only."""

triplestore_url = os.environ.get("CONN_URL", "localhost")
"""CONN_URL: Url of the Triple Store. Defaults to localhost, but is overwritten with the env file when using Docker.
"""

triplestore_port = int(os.environ.get("CONN_PORT", 8890))
"""CONN_PORT: Port of the Triple Store.
Virtuoso Default is 8890
"""

triplestore_db = os.environ.get("CONN_DATABASE", "GOLEM")
"""CONN_DATABASE: Name of the Database in the Triple Store
"""

triplestore_user = os.environ.get("CONN_USER", "dba")
"""CONN_USER: User name to use to connect to Triplestore
"""

triplestore_pwd = os.environ.get("CONN_PASSWORD", "admin")
"""CONN_PASSWORD: User name to use to connect to Triplestore
"""


# Establish a connection to the Triple Store with the designated class "DB"
# TODO: test, if the connection was successfully established. Although, the __init__ will raise an error
db = DB(
    triplestore=triplestore_name,
    protocol=triplestore_protocol,
    url=triplestore_url,
    port=str(triplestore_port),
    username=triplestore_user,
    password=triplestore_pwd,
    database=triplestore_db)

# Setup of the corpora
# Need to instantiate the corpora here!
# TODO: fix this!
corpora = None

# Setup of flask API
api = flask.Flask(__name__)
# enable UTF-8 support
api.config["JSON_AS_ASCII"] = False


@api.route("/", methods=["GET"])
def swagger_ui():
    """Displays the OpenAPI Documentation of the API"""
    return send_from_directory("static/swagger-ui", "index.html")


@api.route("/info", methods=["GET"])
def get_info():
    """Information about the API

    TODO: add information on the current database connection.
    ---
    get:
        summary: About the service
        description: Returns information about the service's API
        operationId: get_info
        responses:
            200:
                description: Information about the API
                content:
                    application/json:
                        schema: ApiInfo
    """

    data = dict(
        name="GOLEM 2 DraCor API",
        version=service_version,
        description="Connects GOLEM to a DraCor-like Frontend"
    )
    # To make sure, that the response matches the schema defined in the OpenAPI
    # we validate this data using the InfoResponse Schema.
    schema = ApiInfo()
    schema.load(data)

    return jsonify(schema.dump(data))


@api.route("/corpora", methods=["GET"])
def get_corpora():
    """Lists available corpora

    ---
    get:
        summary: List available corpora
        description: Returns a list of available corpora
        operationId: get_corpora
        parameters:
            -   in: query
                name: include
                description: Include additional information, e.g. corpus metrics.
                required: false
                example: metrics
                schema:
                    type: string
                    enum:
                        - metrics
        responses:
            200:
                description: Available corpora.
                content:
                    application/json:
                        schema:
                            type: array
                            items: CorpusMetadata
            400:
                description: Invalid value of parameter "include".
                content:
                    text/plain:
                        schema:
                            type: string
    """
    if "include" in request.args:
        param_include = str(request.args["include"])
    else:
        param_include = None

    if param_include:
        if param_include == "metrics":
            #TODO: fix this here!
            #response_data = corpora.list_corpora(include_metrics=True)
            response_data = None
        else:
            response_data = None
            return Response(f"{str(request.args['include'])} is not a valid value of parameter 'include'.", status=400,
                            mimetype="text/plain")
    else:
        # TODO: fix this here
        #response_data = corpora.list_corpora()
        response_data = None

    # TODO: validate against response schema
    return jsonify(response_data)

# End of the API Endpoints


# Generate the OpenAPI Specification
# This can not be moved to the apidoc module,
# because to generate the Documentation, we need the flask API to be runnable
with api.test_request_context():
    spec.path(view=get_info)

# write the OpenAPI Specification as YAML to the root folder
with open('openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification to the /static folder to use in the Swagger UI
with open('static/swagger-ui/openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=service_port)
