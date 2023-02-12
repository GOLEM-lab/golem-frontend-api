# start by pulling the python image
FROM python:3.9-slim

#set the (default) environment variables
ENV SERVICE_URL="http://localhost"
ENV SERVICE_PORT=5000
ENV SERVICE_DEBUG=FALSE

#settings of the POSTDATA (PD) Triplestore connection
ENV PD_TRIPLESTORE="stardog"
ENV PD_PROTOCOL="http"
ENV PD_URL="localhost"
ENV PD_PORT="5820"
ENV PD_DATABASE="PD_KG"
ENV PD_USER="admin"
ENV PD_PASSWORD="admin"

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
COPY util.py /api
COPY sparql.py /api
COPY corpora.py /api
COPY corpus.py /api
COPY poem.py /api
COPY author.py /api
COPY pd_stardog_queries.py /api
COPY pd_corpora.py /api
COPY pd_corpus.py /api
COPY pd_poem.py /api
COPY pd_author.py /api

# configure the container to run in an executed manner
ENTRYPOINT [ "python", "/api/api.py" ]
