# golem-api
A [DraCor](https://dracor.org) powered GOLEM-API

The data is stored in a Virtuoso Triple store (use https://hub.docker.com/r/openlink/virtuoso-opensource-7). 
For testing purposes use the file `data/generated_example_data.ttl`. This data was generated with the Jupyter 
Notebook [generate_test_data](generate_test_data.ipynb).

See the notebook [Howto](Howto.ipynb) for a Tutorial on how to use the tool.

The frontend can be found at https://github.com/GOLEM-lab/golem-corpora-frontend.

# Run the API

### Docker

Our [docker compose file](compose.yaml) makes it easy to run the service in a
docker container:

```sh
docker compose up
```

The interactive OpenAPI documentation of the API can be found at http://localhost:5000.

### Python

```sh
python3 -m venv venv
source venv/bin/activate
pip3 freeze > requirements.txt
```

## See also
The system is an adapted version of the [*POSTDATA 2 DraCor API*](https://github.com/dracor-org/poecor-api).
On the general setup and the idea behind this API see the [CLS INFRA](https://clsinfra.io) Deliverable 
[D7.1 *On Programmable Corpora*](https://doi.org/10.5281/zenodo.7664964). 

## Acknowledgments

The development of this tool was supported by Computational
Literary Studies Infrastructure (CLS INFRA) through its Transnational
Access Fellowship programme. CLS INFRA has received funding from the
European Union’s Horizon 2020 research and innovation programme under
grant agreement №101004984.

