from sparql import DB
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD
from sparql_queries import GolemQuery


class Author:
    """GOLEM Author

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the author
        id (str): ID of the author
        name (str): Name of the author
        refs (list): Identifiers in External Reference Ressources
    """
    # Database connection
    database = None

    uri = None

    id = None

    name = None

    refs = None
    """
    [{"ref": "Q34660", "type": "wikidata"}]
    """

    def __init__(self,
                 database: DB = None,
                 uri: str = None,
                 id: str = None,
                 name: str = None,
                 refs: list = None
                 ):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
            uri (str): URI of the author
            id (str): ID of the author
            name (str): Name of the author
            refs (list): Identifiers in external reference ressources
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

        if name:
            self.name = name

        if refs:
            self.refs = refs


    def generate_graph(self) -> Graph:
        """Generate graph data of an author.

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

        g.add((URIRef(self.uri), RDF.type, CRM.E39_Actor))

        # id
        if self.id:
            id_uri = self.uri + "/id"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(id_uri)))

            g.add((URIRef(id_uri), RDF.type, CRM.E42_Identifier))
            g.add((URIRef(id_uri), CRM.P1i_identifies, URIRef(self.uri)))
            g.add((URIRef(id_uri), CRM.P2_has_type, TYPE.id))
            g.add((URIRef(id_uri), RDF.value, Literal(self.id)))

        if self.name:
            g.add((URIRef(self.uri), RDFS.label, Literal(self.name)))

            name_uri = self.uri + "/name"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(name_uri)))

            g.add((URIRef(name_uri), RDF.type, CRM.E41_Appellation))
            g.add((URIRef(name_uri), CRM.P1i_identifies, URIRef(self.uri)))
            g.add((URIRef(name_uri), CRM.P2_has_type, TYPE.author_name))
            g.add((URIRef(name_uri), RDF.value, Literal(self.name)))

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