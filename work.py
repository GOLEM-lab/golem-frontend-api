from sparql import DB
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD
from sparql_queries import GolemQuery


class Work:
    """GOLEM Work

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the work
        id (str): ID of the work
        title (str): Title
        characters (list): Characters
        authors (list): Authors
        dates (dict): Dates
        refs (list): Identifiers in external reference ressources
        corpus_ids (list): IDs of the parent corpus
    """
    # Database connection
    database = None

    uri = None

    id = None

    title = None

    characters = None
    """
    [
    {
        "id": "character_id",
        "uri" : "character_uri",
        "effect": "created",
        "data" : Character()
    }
    ]
    """

    authors = None
    """
    [
    {
        "id": "author_id",
        "uri": "author_uri",
        "data" : Author()
    }
    ]
    """

    dates = None
    """
    {
    "created": 1997
    }
    """

    refs = None
    """
        [{"ref": "QXXXXX", "type": "wikidata"}]
        """

    corpus_ids = None

    def __init__(self,
                 database: DB = None,
                 uri: str = None,
                 id: str = None,
                 title: str = None,
                 characters: list = None,
                 authors: list = None,
                 dates: dict = None,
                 refs: list = None,
                 corpus_ids: list = None
                 ):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
            uri (str): URI of the work
            id (str): ID of the work
            title (str): Title
            characters (list): Characters
            authors (list): Authors
            dates (dict): Dates
            refs (list): IDs in external reference ressources
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

        if title:
            self.title = title

        if characters:
            self.characters = characters

        if authors:
            self.authors = authors

        if dates:
            self.dates = dates

        if refs:
            self.refs = refs

        if corpus_ids:
            self.corpus_ids = corpus_ids

    def generate_graph(self) -> Graph:
        """Generate graph data of work.

        We use that for creating test data.
        """

        # needed for the prefixes
        golem_query = GolemQuery()
        CRM = Namespace(golem_query.get_prefix_uri("crm"))
        CLS = Namespace(golem_query.get_prefix_uri("cls"))
        TYPE = Namespace(golem_query.get_prefix_uri("gt"))
        GO = Namespace(golem_query.get_prefix_uri("go"))
        GD = Namespace(golem_query.get_prefix_uri("gd"))
        LRM = Namespace(golem_query.get_prefix_uri("lrm"))

        g = Graph()
        # add the prefixes
        for item in golem_query.prefixes:
            g.namespace_manager.bind(item["prefix"], URIRef(item["uri"]))

        g.add((URIRef(self.uri), RDF.type, LRM.F1_Work))

        if self.id:
            id_uri = self.uri + "/id"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(id_uri)))

            g.add((URIRef(id_uri), RDF.type, CRM.E42_Identifier))
            g.add((URIRef(id_uri), CRM.P1i_identifies, URIRef(self.uri)))
            g.add((URIRef(id_uri), CRM.P2_has_type, TYPE.id))
            g.add((URIRef(id_uri), RDF.value, Literal(self.id)))

        if self.title:
            g.add((URIRef(self.uri), RDFS.label, Literal(self.title)))

            title_uri = self.uri + "/title"
            g.add((URIRef(self.uri), CRM.P102_has_title, URIRef(title_uri)))

            g.add((URIRef(title_uri), RDF.type, CRM.E35_Title))
            g.add((URIRef(title_uri), CRM.P102i_is_title_of, URIRef(self.uri)))
            g.add((URIRef(title_uri), RDF.value, Literal(self.title)))

        # F27 Work Creation
        work_creation_uri = self.uri + "/creation"
        g.add((URIRef(work_creation_uri), RDF.type, LRM.F27_Work_Creation))

        # created the characters
        if self.characters:
            for character_item in self.characters:
                # only if the work created the character:
                if "effect" in character_item:
                    if character_item["effect"] == "created":
                        if "uri" in character_item:
                            character_uri = character_item["uri"]
                        elif "id" in character_item:
                            character_uri = golem_query.get_prefix_uri("gd") + character_item["id"]
                        else:
                            character_uri = None

                        if character_uri:
                            g.add((URIRef(work_creation_uri), CRM.P94_has_created, URIRef(character_uri)))
                            g.add((URIRef(character_uri), CRM.P94i_was_created_by, URIRef(work_creation_uri)))

        # created the work
        g.add((URIRef(work_creation_uri), LRM.R16_created, URIRef(self.uri)))
        g.add((URIRef(self.uri), LRM.R16i_was_created_by, URIRef(work_creation_uri)))

        if self.authors:
            for author_item in self.authors:
                if "uri" in author_item:
                    author_uri = author_item["uri"]
                elif "id" in author_item:
                    author_uri = golem_query.get_prefix_uri("gd") + author_item["id"]
                else:
                    author_uri = None

                if author_uri:
                    g.add((URIRef(work_creation_uri), CRM.P14_carried_out_by, URIRef(author_uri)))
                    g.add((URIRef(author_uri), CRM.P14i_performed, URIRef(work_creation_uri)))

        # Time-Span
        if self.dates:
            if "created" in self.dates:
                ts_uri = work_creation_uri + "/ts"
                g.add((URIRef(work_creation_uri), CRM["P4_has_time-span"], URIRef(ts_uri)))
                g.add((URIRef(ts_uri), CRM["P4i_is_time-span_of"], URIRef(work_creation_uri)))

                g.add((URIRef(ts_uri), RDF.type, CRM["E52_Time-Span"]))
                # this is cheeting. Maybe there is a more CIDOC-ish way to do it.
                g.add((URIRef(ts_uri), RDF.value, Literal(self.dates["created"])))

        # Wikidata id
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

        return g
