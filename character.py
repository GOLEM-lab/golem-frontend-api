from sparql import DB
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD
from sparql_queries import GolemQuery


class Character:
    """GOLEM Character

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the character
        id (str): ID of the character
        character_type (str): Type of the character. Values are "fanon" or "canon"
        name (str): Name of the character
        gender (str): Gender of the character. Values are "male", "female", "nonbinary"
        entry_name (str): Entry Name ?
        refs (list): Links to external reference resources
        source (dict): Information on the source
        years (dict): Information on years
        metrics (dict): Character Metrics
        corpus_ids (list): IDs of the parent corpus
    """
    # Database connection
    database = None

    uri = None

    id = None

    character_type = None

    name = None

    gender = None

    entry_name = None

    refs = None

    source = None

    years = None

    metrics = None

    corpus_ids = None

    def __init__(self,
                 database: DB = None,
                 uri: str = None,
                 id: str = None,
                 character_type: str = None,
                 name: str = None,
                 gender: str = None,
                 entry_name: str = None,
                 source: dict = None,
                 years: dict = None,
                 metrics: dict = None,
                 refs: list = None,
                 corpus_ids: list = None
                 ):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
            uri (str): URI of the corpus
            id (str): ID of the corpus
            character_type (str): Type of character. Values are "canon" or "fanon".
            name (str): Name of the character
            gender (str): Gender. Values: "male", "female", "nonbinary"
            entry_name (str): Entry Name?
            source (dict): Information on source
            years (dict): Information on years
            metrics (dict): Character metrics
            refs (list): Links to external Reference Resources
            corpus_ids (list): IDs of the corpora the character is contained in
        """
        if database:
            self.database = database

        if uri:
            self.uri = uri

        if id:
            self.id = id
        else:
            pass
            # try to SPARQL the ID
            # try:
                # self.get_id()
            # except:
                # pass

        if character_type:
            self.character_type = character_type

        if name:
            self.name = name

        if gender:
            self.gender = gender

        if entry_name:
            self.entry_name = entry_name

        if source:
            self.source = source

        if years:
            self.years = years

        if metrics:
            self.metrics = metrics

        if refs:
            self.refs = refs

        if corpus_ids:
            self.corpus_ids = corpus_ids

    def generate_graph(self) -> Graph:
        """Generate graph data of character.

        We use that for creating test data.
        """

        # needed for the prefixes
        golem_query = GolemQuery()
        CRM = Namespace(golem_query.get_prefix_uri("crm"))
        CLS = Namespace(golem_query.get_prefix_uri("cls"))
        TYPE = Namespace(golem_query.get_prefix_uri("gt"))
        GO = Namespace(golem_query.get_prefix_uri("go"))

        g = Graph()
        # add the prefixes
        for item in golem_query.prefixes:
            g.namespace_manager.bind(item["prefix"], URIRef(item["uri"]))

        if self.uri:
            g.add((URIRef(self.uri), RDF.type, GO.C1_Character_Concept))

        # ID of character
        # TODO: this pattern should be reused
        if self.id:
            id_uri = self.uri + "/id"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(id_uri)))

            # Corpus ID as Identifier
            g.add((URIRef(id_uri), RDF.type, CRM.E42_Identifier))
            g.add((URIRef(id_uri), CRM.P2_has_type, TYPE.id))
            g.add((URIRef(id_uri), RDF.value, Literal(self.id)))

        if self.name:
            g.add((URIRef(self.uri), RDFS.label, Literal(self.name)))

            name_uri = self.uri + "/character_name"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(name_uri)))

            # Name as Appellation
            g.add((URIRef(name_uri), RDF.type, CRM.E41_Appellation))
            g.add((URIRef(name_uri), CRM.P2_has_type, TYPE.character_name))
            g.add((URIRef(name_uri), RDF.value, Literal(self.name)))

        if self.character_type:
            g.add((URIRef(self.uri), CRM.P2_has_type, TYPE[self.character_type + "_character"]))

        if self.gender:
            g.add((URIRef(self.uri), CRM.P2_has_type, TYPE["gender/" + self.gender]))

        # TODO: entry name

        return g

