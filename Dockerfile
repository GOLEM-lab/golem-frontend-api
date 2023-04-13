# start by pulling the python image
FROM python:3.9-slim

#set the (default) environment variables
ENV SERVICE_URL="http://localhost"
ENV SERVICE_PORT=5000
ENV SERVICE_DEBUG=FALSE

#settings of the Triplestore connection
ENV CONN_TRIPLESTORE="virtuoso"
ENV CONN_PROTOCOL="http"
ENV CONN_URL="localhost"
ENV CONN_PORT="8890"
ENV CONN_USER="dba"
ENV CONN_PASSWORD="admin"

#create a directory for the api
CMD mkdir /api

# copy the requirements file
COPY ./requirements.txt /api/requirements.txt

# switch working directory
WORKDIR /api

# install the dependencies and packages
RUN pip install -r requirements.txt

# copy local files to container
CMD ls
COPY api.py /api
COPY static /api/static
COPY apidoc.py /api
COPY schemas.py /api
COPY sparql.py /api
COPY sparql_queries.py /api
COPY corpora.py /api
COPY corpus.py /api

# configure the container to run in an executed manner
ENTRYPOINT [ "python", "/api/api.py" ]
