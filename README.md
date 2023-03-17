# poecor-api

API to POSTDATA's infrastructure

POSTDATA's data is stored in a [Stardog](https://www.stardog.com/get-started/)
triple store (https://postdata.linhd.uned.es). The PoeCor API acts as a
middleware that sends SPARQL queries to the backend and exposes a REST API.
See https://poecor.org/api.

Generic API:

* List corpora
* List poems
* Get details of poem

SPARQL Queries currently available: https://github.com/linhd-postdata/knowledge-graph-queries
Triple Store: https://github.com/linhd-postdata/postdata-stardog

## Local development

The PoeCor API expects several environment variables, among them the credentials
for the POSTDATA triple store. To set those up copy `dev.env.sample` to
`dev.env` and edit the `PD_USER` and `PD_PASSWORD` variables:

```sh
cp dev.env.sample dev.env
# now edit dev.env
```

### Docker

Our [docker compose file](compose.yaml) makes it easy to run the service in a
docker container:

```sh
docker compose up
```

Open http://localhost:5000 in a browser.

### Python

```sh
python3 -m venv venv
source venv/bin/activate
pip3 freeze > requirements.txt
```

## See also

The [PoeCor frontend](https://github.com/dracor-org/poecor-frontend) is a web
interface that provides a limited [dracor-like](https://dracor.org) view of
poetic corpora.
