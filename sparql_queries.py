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
            "uri": "http://data.golemlab.eu/data/"
        },
        {
            "prefix": "gt",
            "uri": "http://data.golemlab.eu/data/entity/type/"
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
            "prefix": "lrm",
            "uri": "http://www.cidoc-crm.org/cidoc-crm/lrmoo/"
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


class CorporaUrisNames(GolemQuery):
    """SPARQL Query: URIs and Corpus Names of all Corpora"""

    label = "URIs and Names of Corpora"

    description = """
    Get URIs and Names of corpora (cls:X1_Corpus) in the Knowledge Graph.
    """

    query = """
    SELECT ?corpus_uri, ?corpus_name WHERE {
        ?corpus_uri a cls:X1_Corpus ;
            crm:P1_is_identified_by ?nameID .
        
        ?nameID crm:P2_has_type gt:corpus_name ; 
            rdf:value ?corpus_name .
    }
    """


class CorporaUrisIds(GolemQuery):
    """SPARQL Query: URIs and Corpus Ids of all Corpora"""

    label = "URIs and IDs of Corpora"

    description = """
    Get URIs and IDs of corpora (cls:X1_Corpus) in the Knowledge Graph.
    """

    query = """
    SELECT ?corpus_uri, ?corpus_id WHERE {
        ?corpus_uri a cls:X1_Corpus ;
            crm:P1_is_identified_by ?nodeID .

        ?nodeID crm:P2_has_type gt:id ; 
            rdf:value ?corpus_id .
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

        ?nameID crm:P2_has_type gt:corpus_name ; 
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


class CorpusId(GolemQuery):
    """SPARQL Query: ID by CorpusURI"""

    label = "ID of Corpus"

    description = """
    Get ID of a corpus identified by an URI.
    """

    template = """
    SELECT ?id WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P1_is_identified_by ?node .

        ?node crm:P2_has_type gt:id ; 
            rdf:value ?id .
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]


class CorpusAcronym(GolemQuery):
    """SPARQL Query: Acronym by CorpusURI"""

    label = "Acronym of Corpus"

    description = """
    Get acronym of a corpus identified by an URI.
    """

    template = """
    SELECT ?acronym WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P1_is_identified_by ?acronymID .

        ?acronymID crm:P2_has_type gt:corpus_acronym ;
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


class CorpusDescription(GolemQuery):
    """SPARQL Query: Description by CorpusURI"""

    label = "Description of Corpus"

    description = """
    Get description of a corpus identified by an URI.
    """

    template = """
    SELECT ?description WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P3_has_note ?description .
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]


class CorpusLicence(GolemQuery):
    """SPARQL Query: Licence by CorpusURI"""

    label = "Licence data of Corpus"

    description = """
    Get licence data of a corpus identified by an URI.
    """

    template = """
    SELECT ?uri ?name WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P104_is_subject_to ?licence .
        
        ?licence a crm:E30_Right;
            crm:P3_has_note ?name ;
            crm:P67_refers_to ?uri .
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

        ?nameID crm:P2_has_type gt:corpus_name ; 
            rdf:value ?name .
            
        ?acronymID crm:P2_has_type gt:corpus_acronym ;
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


class CorpusCharacterConceptUris(GolemQuery):
    """SPARQL Query: URIs of Character in a Corpus"""

    label = "Corpus Character URIs"

    description = """
    Get URIs of Characters (go:C1_Character_Concept) of a single corpus in the Knowledge Graph.
    """

    query = """
    SELECT ?character_uri WHERE {
        <$1> a cls:X1_Corpus ;
            crm:P148_has_component ?character_uri.

        ?character_uri a go:C1_Character_Concept . 
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]


class EntityId(GolemQuery):
    """SPARQL Query: ID by URI"""

    label = "ID of an Entity"

    description = """
    Generic query to get ID of an entity identified by an URI.
    It identifies the node that holds the ID as value by the type "id" (gt:id).
    """

    template = """
    SELECT ?id WHERE {
        <$1> crm:P1_is_identified_by ?identifier .

        ?identifier a crm:E42_Identifier ;
            crm:P2_has_type gt:id ; 
            rdf:value ?id .
    }
    """

    variables = [
        {
            "id": "entity_uri",
            "class": "crm:E1_CRM_Entity",
            "description": "URI of an Entity."
        }
    ]


class CharacterName(GolemQuery):
    """SPARQL Query: Character Name by URI"""

    label = "Name of a character"

    description = """
    Get the name (E41_Appellation) of a character.
    """

    template = """
    SELECT ?name WHERE {
        <$1> crm:P1_is_identified_by ?appellation .

        ?appellation a crm:E41_Appellation ;
            crm:P2_has_type gt:character_name ; 
            rdf:value ?name .
    }
    """

    variables = [
        {
            "id": "character_uri",
            "class": "go:C1_Character_Concept",
            "description": "URI of a Character."
        }
    ]


class CorpusCharactersUriIdName(GolemQuery):
    """SPARQL Query: Get character URI, ID and Name for a corpus"""

    label = "Character data (uri, id, name) of corpus"

    description = """
    Get character data (uri, id, optionally name) of a single corpus."""

    template = """
    SELECT ?character AS ?uri ?id ?name WHERE {
        ?character a go:C1_Character_Concept ;
        crm:P148i_is_component_of <$1> ;
        crm:P1_is_identified_by ?identifier.

        ?identifier crm:P2_has_type gt:id;
            rdf:value ?id .

        OPTIONAL {
            ?character crm:P1_is_identified_by ?appellation .
            
            ?appellation a crm:E41_Appellation;
                crm:P2_has_type gt:character_name;
                rdf:value ?name.
        }
    }
    """

    variables = [
        {
            "id": "corpus_uri",
            "class": "cls:X1_Corpus",
            "description": "URI of a Corpus."
        }
    ]


