# golem-api

DraCor-style API to GOLEMs Triple Store

GOLEM data is stored in Virtuoso

Generic API:

* List corpora and metrics

Triple Store: Virtuoso (use https://hub.docker.com/r/openlink/virtuoso-opensource-7)

### Docker

Our [docker compose file](compose.yaml) makes it easy to run the service in a
docker container:

```sh
docker compose up
```


### Python

```sh
python3 -m venv venv
source venv/bin/activate
pip3 freeze > requirements.txt
```

## Data
Example data is in `/data`. Upload to Vituoso to named graph `https://golemlab.eu/data`. 
SPARQL Query Interface of Virtuoso: http://localhost:8890/sparql

```
SELECT * FROM <https://golemlab.eu/data> WHERE {
?s ?p ?o .
}
```

## See also


## Acknowledgments

The development of this tool was supported by Computational
Literary Studies Infrastructure (CLS INFRA) through its Transnational
Access Fellowship programme. CLS INFRA has received funding from the
European Union’s Horizon 2020 research and innovation programme under
grant agreement №101004984.

