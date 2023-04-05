import flask
from flask import jsonify, Response, send_from_directory, request
from apidoc import spec, ApiInfo, CorpusMetadata, PoemMetadata
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

triplestore_name = str(os.environ.get("PD_TRIPLESTORE", "stardog"))
"""PD_TRIPLESTORE: Name of the Triple Store.
Default implementation is based on Stardog.
"""

triplestore_protocol = os.environ.get("PD_PROTOCOL", "http")
"""PD_PROTOCOL: Postdata's current implementation uses http only."""

triplestore_url = os.environ.get("PD_URL", "localhost")
"""PD_URL: Url of the Triple Store. Defaults to localhost, but is overwritten with the env file when using Docker.
"""

triplestore_port = int(os.environ.get("PD_PORT", 5820))
"""PD_PORT: Port of the Triple Store.
Stardog Default is 5820
"""

triplestore_db = os.environ.get("PD_DATABASE", "PD_KG")
"""PD_DATABASE: Name of the Database in the Triple Store
"""

triplestore_user = os.environ.get("PD_USER", "admin")
"""PD_USER: User name to use to connect to Triplestore
"""

triplestore_pwd = os.environ.get("PD_PASSWORD", "admin")
"""PD_PASSWORD: User name to use to connect to Triplestore
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
# the demonstrator uses only one corpus with the name "postdata" because POSTDATA project has not structured their data
# into corpora/collections but added everything to a single graph. We treat this graph as a single corpus, still
# the setup of the API would allow for multiple corpora
corpora = PostdataCorpora(database=db)

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
            response_data = corpora.list_corpora(include_metrics=True)
        else:
            response_data = None
            return Response(f"{str(request.args['include'])} is not a valid value of parameter 'include'.", status=400,
                            mimetype="text/plain")
    else:
        response_data = corpora.list_corpora()

    # TODO: validate against response schema
    return jsonify(response_data)


@api.route("/corpora/<path:corpusname>", methods=["GET"])
def get_corpus_metadata(corpusname:str):
    """Corpus Metadata

    Args:
        corpusname: ID/name of the corpus, e.g. "postdata".

    ---
    get:
        summary: Corpus Metadata
        description: Returns metadata on a corpus. Unlike the DraCor API the response does not contain information
            on included corpus items (poems). Use the endpoint ``/corpora/{corpusname}/poems`` instead.
        operationId: get_corpus_metadata
        parameters:
            -   in: path
                name: corpusname
                description: Name/ID of the corpus.
                required: true
                example: postdata
                schema:
                    type: string
        responses:
            200:
                description: Corpus metadata.
                content:
                    application/json:
                        schema: CorpusMetadata
            404:
                description: No such corpus. Parameter ``corpusname`` is invalid. A list of valid values can be
                    retrieved via the ``/corpora`` endpoint.
                content:
                    text/plain:
                        schema:
                            type: string
    """
    if corpusname in corpora.corpora:
        metadata = corpora.corpora[corpusname].get_metadata(include_metrics=True)

        # Validate response with schema "CorpusMetadata"
        schema = CorpusMetadata()
        schema.load(metadata)

        return jsonify(schema.dump(metadata))

    else:
        return Response(f"No such corpus: {corpusname}", status=404,
                        mimetype="text/plain")

# End of the API Endpoints


# Generate the OpenAPI Specification
# This can not be moved to the apidoc module,
# because to generate the Documentation, we need the flask API to be runnable
with api.test_request_context():
    spec.path(view=get_info)
    spec.path(view=get_corpora)
    spec.path(view=get_corpus_metadata)

# write the OpenAPI Specification as YAML to the root folder
with open('openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification to the /static folder to use in the Swagger UI
with open('static/swagger-ui/openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=service_port)
