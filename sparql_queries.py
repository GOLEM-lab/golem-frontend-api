from sparql import SparqlQuery

"""Here will all the classes = queries go that are then imported into the api
"""


# Set globally for all SPARQL Queries against the GOLEM infrastructure
class GolemQuery(SparqlQuery):
    """SPARQL Query to GOLEMs Virtuoso
    """

    # set globally for all queries to GOLEM's Virtuoso

    # Queries work only with the stardog implementation (because of the union graph)
    scope = "virtuoso"

    # Prefixes in SPARQL Queries
    prefixes = [
        {
            "prefix": "gd",
            "uri": "http://golemlab.eu/data/"
        },
        {
            "prefix": "crm",
            "uri": "http://www.cidoc-crm.org/cidoc-crm/"
        },
        {
            "prefix": "owl",
            "uri": "http://www.w3.org/2002/07/owl#"
        },
        {
            "prefix": "xsd",
            "uri": "http://www.w3.org/2001/XMLSchema#"
        },
        {
            "prefix": "cls",
            "uri": "http://clscor.io/ontology/"
        },
        {
            "prefix": "go",
            "uri": "http://golemlab.eu/ontology/"
        },
        {
            "prefix": "rdfs",
            "uri": "http://www.w3.org/2000/01/rdf-schema#"
        },
        {
            "prefix": "nif",
            "uri": "http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#"
        }
    ]


class CorporaUris(GolemQuery):
    """SPARQL Query: URIs of all Corpora"""

    label = "URIs of Corpora"

    description = """
    Get URIs of corpora (cls:X1_Corpus) in the Knowledge Graph.
    """

    query = """
    SELECT ?corpus_uri WHERE {
        ?corpus_uri a cls:X1_Corpus . 
    }
    """


class CorpusName(GolemQuery):
    """SPARQL Query: Name by CorpusURI"""

    label = "Name of Corpus"

    description = """
    Get name of a corpus identified by an URI.
    """

    template = """
    SELECT ?name WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P1_is_identified_by ?nameID .

        ?nameID crm:P2_has_type <http://golemlab.eu/data/entity/type/corpus_name> ; 
            rdf:value ?name .
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]

class CorpusNameAcronym(GolemQuery):
    """SPARQL Query: Name and Acronym by CorpusURI"""

    label = "Name and Acronym of Corpus"

    description = """
    Get name and acronym of a corpus identified by an URI.
    """

    template = """
    SELECT ?name ?acronym WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P1_is_identified_by ?nameID, ?acronymID .

        ?nameID crm:P2_has_type <http://golemlab.eu/data/entity/type/corpus_name> ; 
            rdf:value ?name .
            
        ?acronymID crm:P2_has_type <http://golemlab.eu/data/entity/type/corpus_acronym> ;
            rdf:value ?acronym .
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]


class CorpusMetrics(GolemQuery):
    """SPARQL Query: Metrics of a single Corpus"""

    label = "Corpus Metrics"

    description = """
    Get all metrics of a corpus identified by URI
    """

    template = """
        SELECT ?dimensionURI ?value WHERE {
            <$1> crm:P43_has_dimension ?dimensionURI .
            ?dimensionURI crm:P90_has_value ?value .
            ?dimensionURI rdfs:label ?dimension .
        }
        """
    # <$1> is the variable, that can be replaced with method inject(["full uri here"])

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]
