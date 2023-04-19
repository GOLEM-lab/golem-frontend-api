from sparql import DB
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD
from sparql_queries import GolemQuery
from schemas import CharacterSchema


class Character:
    """GOLEM Character

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the character
        id (str): ID of the character
        character_type (str): Type of the character. Values are "fanon" or "canon"
        name (str): Name of the character
        gender (str): Gender of the character. Values are "male", "female", "nonbinary"
        refs (list): Links to external reference resources
        source (dict): Information on the source
        years (dict): Information on years
        refs (list): IDs in external reference resources
        relations (list): Relations of the character
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

    refs = None

    source = None

    years = None

    refs = None

    relations = None

    metrics = None

    corpus_ids = None

    def __init__(self,
                 database: DB = None,
                 uri: str = None,
                 id: str = None,
                 character_type: str = None,
                 name: str = None,
                 gender: str = None,
                 source: dict = None,
                 years: dict = None,
                 metrics: dict = None,
                 refs: list = None,
                 relations = None,
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
            source (dict): Information on source
            years (dict): Information on years
            metrics (dict): Character metrics
            refs (list): Links to external Reference Resources
            relations (list): Character relations
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

        if source:
            self.source = source

        if years:
            self.years = years

        if metrics:
            self.metrics = metrics

        if refs:
            self.refs = refs

        if relations:
            self.relations = relations

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
        GD = Namespace(golem_query.get_prefix_uri("gd"))

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

        # External Reference Resource (Wikidata)
        if self.refs:
            # get the wikidata id(s)
            filtered_refs = list(filter(lambda ref: "wikidata" in ref["type"], self.refs))
            if len(filtered_refs) == 1:
                # one single wikidata id, otherwise it doesn't make sense
                q = filtered_refs[0]["ref"]
                wd_id_uri = self.uri + "/wd"

                g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(wd_id_uri)))
                g.add((URIRef(wd_id_uri), RDF.type, CRM.E42_Identifier))
                g.add((URIRef(wd_id_uri), CRM.P1i_identifies, URIRef(self.uri)))
                g.add((URIRef(wd_id_uri), CRM.P2_has_type, TYPE.wikidata))
                g.add((URIRef(wd_id_uri), RDF.value, Literal(q)))

        # Corpus ids
        # Corpora, that the character is part of
        if self.corpus_ids:
            for corpus_id in self.corpus_ids:
                # TODO: evaluate if this is the best idea to model it.
                g.add((GD[corpus_id], CRM.P148_has_component, URIRef(self.uri)))
                g.add((URIRef(self.uri), CRM.P148i_is_component_of, GD[corpus_id]))

        # Relations, e.g. derivative of
        if self.relations:
            # only focus on the "derivative_of" type of now:
            filtered_relations = list(filter(lambda rel: "derivative_of" in rel["type"], self.relations))

            for item in filtered_relations:
                g.add((URIRef(self.uri), CRM.P130_shows_features_of, URIRef(golem_query.get_prefix_uri("gd") + item["id"])))
                g.add((URIRef(golem_query.get_prefix_uri("gd") + item["id"]), CRM.P130i_features_are_also_found_on, URIRef(self.uri)))

        return g

    def get_metadata(self, validation: bool = False) -> dict:
        """Serialize Character Metadata.

        Args:
            validation (bool, optional): Validate with schema "CharacterSchema".

        Returns:
            dict: Serialization of the character metadata.
        """

        metadata = dict(
            id=self.id,
            uri=self.uri
        )

        # TODO: implement:
        """
                id = fields.Str()
            uri = fields.Str()
            characterType = fields.Str(validate=validate.OneOf(["canon", "fanon"]))
            characterName = fields.Str()
            characterGender = fields.Str(validate=validate.OneOf(["male", "female", "nonbinary"]))
            refs = fields.Nested(ExternalReferenceSchema, required=False)
            sourceName = fields.Str()
            sourceUrl = fields.Str()
            createdYear = fields.Int()
            firstFanficYear = fields.Int()
            numDocuments = fields.Int()
            characterCsvUrl = fields.Str()
            authors = fields.Nested(AuthorSchema)
                """

        if validation:
            try:
                schema = CharacterSchema()
                schema.load(metadata)
            except:
                raise Exception("Could not validate metadata!")

        return metadata
