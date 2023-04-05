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

## See also

