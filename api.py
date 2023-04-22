import flask
from flask import jsonify, Response, send_from_directory, request
from apidoc import spec
from schemas import ApiInfoSchema, CorpusSchema
from sparql import DB
from corpora import Corpora
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

triplestore_user = os.environ.get("CONN_USER", "dba")
"""CONN_USER: User name to use to connect to Triplestore
"""

triplestore_pwd = os.environ.get("CONN_PASSWORD", "admin")
"""CONN_PASSWORD: User name to use to connect to Triplestore
"""

# this is probably not in use
# triplestore_graph = os.environ.get("CONN_GRAPH", "https://golemlab.eu/data")
"""CONN_GRAPH: Default named graph where data is stored
"""

# Establish a connection to the Triple Store with the designated class "DB"
# TODO: test, if the connection was successfully established. Although, the __init__ will raise an error
# removed graph=triplestore_graph
db = DB(
    triplestore=triplestore_name,
    protocol=triplestore_protocol,
    url=triplestore_url,
    port=str(triplestore_port),
    username=triplestore_user,
    password=triplestore_pwd
)


# Setup of the corpora
# Need to instantiate the corpora here!
# TODO fix this
corpora = Corpora(database=db)
# load the corpora
try:
    corpora.load()
except:
    # raise Exception("Can not load corpora. SPARQL endpoint is " + db.sparql_query_endpoint)
    pass

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
                        schema: ApiInfoSchema
    """

    data = dict(
        name="GOLEM 2 DraCor API",
        version=service_version,
        description="Connects GOLEM to a DraCor-like Frontend"
    )
    # To make sure, that the response matches the schema defined in the OpenAPI
    # we validate this data using the InfoResponse Schema.
    schema = ApiInfoSchema()
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
                            items: CorpusSchema
            400:
                description: Invalid value of parameter "include".
                content:
                    text/plain:
                        schema:
                            type: string
    """
    if corpora is None:
        corpora.load()

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


@api.route("/corpora/<path:corpus_id>", methods=["GET"])
def get_corpus_metadata(corpusname: str):
    """Get Metadata on a single corpus

    Args:
        corpus_id: ID of the corpus.

    ---
    get:
        summary: Corpus Metadata
        description: Returns metadata on a corpus. Unlike the DraCor API the response does not contain information
            on included items (works, characters). Use the endpoint ``/corpora/{corpus_id}/characters`` instead.
        operationId: get_corpus_metadata
        summary: Corpus Metadata
        parameters:
            -   in: path
                name: corpus_id
                description: ID of the corpus.
                required: true
                example: potter_corpus
                schema:
                    type: string
        responses:
            200:
                description: Corpus metadata.
                content:
                    application/json:
                        schema: CorpusMetadata
            404:
                description: No such corpus. Parameter ``corpus_id`` is invalid. A list of valid values can be
                    retrieved via the ``/corpora`` endpoint.
                content:
                    text/plain:
                        schema:
                            type: string
    """
    if corpus_id in corpora.corpora:
        metadata = corpora.corpora[corpus_id].get_metadata(include_metrics=True)

        # TODO: Validate response before returning
        # Validate response with schema "CorpusMetadata"
        # schema = CorpusMetadata()
        # schema.load(metadata)

        # return jsonify(schema.dump(metadata))
        return jsonify(metadata)

    else:
        return Response(f"No such corpus: {corpus_id}", status=404,
                        mimetype="text/plain")


@api.route("/corpora", methods=["PUT"])
def trigger_loading_corpora():
    """Trigger Loading of Corpora
    ---
    put:
            summary: Load Corpora
            description: Trigger Loading of Corpora
            operationId: trigger_loading_corpora
            responses:
                200:
                    description: Successfully loaded corpora.
                500:
                    description: Something went wrong. Could not load data.
    """
    try:
        corpora.load()
        return Response("Successfully loaded corpora.", status=200, mimetype="text/plain")
    except:
        return Response("Something went wrong.", status=500, mimetype="text/plain")


@api.route("/db", methods=["POST"])
def ingest_data():
    """Load data into the triple store
        ---
        post:
            summary: Load data
            description: Load data into the triple store
            operationId: ingest_data
            parameters:
            -   in: query
                name: graph
                description: Name of the target graph. Default graph is "https://golemlab.eu/data".
                required: false
                default: https://golemlab.eu/data
                schema:
                    type: string
            requestBody:
                description: Data to load.
                required: true
                content:
                    application/x-turtle:
                        schema:
                            type: string
            responses:
                201:
                    description: Successfully ingested data.
                400:
                    description: No data included in the request body. Can not load data.
                500:
                    description: Something went wrong. Could not load data.
        """
    if "graph" in request.args:
        graph = str(request.args["graph"])
    else:
        graph = "https://golemlab.eu/data"

    data = request.data
    if not data:
        return Response("No data to load.", status=400, mimetype="text/plain")
    try:
        db.upload(data, graph=graph, format="ttl")
        return Response("Successfully ingested data", status=201, mimetype="text/plain")
    except:
        return Response("Something went wrong.", status=500, mimetype="text/plain")


@api.route("/db", methods=["DELETE"])
def delete_graph():
    """Delete a Named Graph
        ---
        delete:
            summary: Delete Named Graph
            description: Delete a named graph from the triple store
            operationId: delete_graph
            parameters:
            -   in: query
                name: graph
                description: Name of the graph to delete. Default graph is "https://golemlab.eu/data".
                required: true
                default: https://golemlab.eu/data
                schema:
                    type: string
            responses:
                200:
                    description: Successfully deleted graph.
                400:
                    description: Graph to delete is not specified.
                500:
                    description: Something went wrong. Could not delete the graph.
        """
    if "graph" in request.args:
        graph = str(request.args["graph"])
    else:
        return Response("Graph to delete is not specified.", status=400, mimetype="text/plain")

    try:
        db.delete_graph(graph)
        return Response("Successfully deleted graph", status=200, mimetype="text/plain")
    except:
        return Response("Something went wrong.", status=500, mimetype="text/plain")

# End of the API Endpoints


# Generate the OpenAPI Specification
# This can not be moved to the apidoc module,
# because to generate the Documentation, we need the flask API to be runnable
with api.test_request_context():
    spec.path(view=get_info)
    spec.path(view=get_corpora)
    spec.path(view=get_corpus_metadata)
    spec.path(view=trigger_loading_corpora)
    spec.path(view=ingest_data)
    spec.path(view=delete_graph)


# write the OpenAPI Specification as YAML to the root folder
with open('openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification to the /static folder to use in the Swagger UI
with open('static/swagger-ui/openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=service_port)
