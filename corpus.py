from sparql import DB
from sparql_queries import CorpusMetrics, CorpusName, CorpusAcronym, CorpusId
from schemas import CorpusSchema
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD
from sparql_queries import GolemQuery


class Corpus:
    """GOLEM Corpus

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the corpus
        id (str): ID of the corpus
        name (str) : Name of the corpus (an identifier; DEPRECATED!!!)
        acronym (str) : Acronym of the corpus
        description (str) : Description of the corpus
        licence (dict) : Licence
        repository (dic) : Repository
        metrics (dict) : Metrics of a corpus
    """
    # Database connection
    database = None

    uri = None

    id = None

    name = None # This is deprecated!

    acronym = None

    # Description of the Corpus
    description = None

    # Licence
    licence = None

    # Repository
    repository = None

    # Metrics of the corpus
    metrics = None

    def __init__(self,
                 database: DB = None,
                 uri: str = None,
                 id: str = None,
                 name: str = None,
                 acronym: str = None,
                 description: str = None,
                 licence: dict = None,
                 repository: dict = None,
                 metrics: dict = None
                 ):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
            uri (str): URI of the corpus
            id (str): ID of the corpus
            name (str): Identifier (name) of the corpus (DEPRECATED!!)
            acronym: Acronym of the corpus
            description (str): Description of the corpus
            licence (dict): Licence Information
            repository (dict): Repository Information
            metrics (dict): Corpus Metrics
        """
        if database:
            self.database = database

        if uri:
            self.uri = uri

        if id:
            self.id = id
        else:
            # try to SPARQL the ID
            try:
                self.get_id()
            except:
                pass

        # Name is somewhat deprecated
        if name:
            self.name = name
        else:
            # try to sparql the name from the knowledge graph
            try:
                self.get_name()
            except:
                pass

        if acronym:
            self.acronym = acronym

        if description:
            self.description = description

        if licence:
            self.licence = licence

        if repository:
            self.repository = repository

        if metrics:
            self.metrics = metrics

    def get_metrics(self, use_mapping: bool = False) -> dict:
        """Assemble and return corpus metrics.

         Uses a SPARQL Query of class "CorpusMetrics" of the module "sparql_queries".

        Args:
            use_mapping (bool): Use a mapping to transform the keys of the metrics dictionary. Defaults to False
        """

        if self.metrics:
            return self.metrics

        else:
            if self.database:
                if self.uri:
                    query = CorpusMetrics()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    metrics = dict()

                    if use_mapping:
                        # map the keys of the results of the SPARQL query; unfortunately, this has to be hardcoded here;
                        # Maybe the label could be included somewhere in the graph istead
                        """
                        'number_of_chapters': 700000,
                        'number_of_characters': 20,
                        'number_of_comments': 123,
                        'number_of_documents': 200000,
                        'number_of_female_characters': 8,
                        'number_of_nonbinary_characters': 2,
                        'number_of_paragraphs': 9000000,
                        'number_of_words-comments': 123000,
                        'number_of_words-text': 2000000000}
                        """
                        mapping = dict(
                            number_of_chapters="chapters",
                            number_of_characters="characters",
                            number_of_comments="comments",
                            number_of_documents="documents",
                            number_of_female_characters="female",
                            number_of_male_characters="male",
                            number_of_nonbinary_characters="nonbinary",
                            number_of_paragraphs="paragraphs"
                        )
                    else:
                        mapping = None

                    for item in results:
                        key_from_graph = item["dimensionURI"].split("/")[-1:][0]
                        if mapping:
                            if key_from_graph in mapping:
                                key = mapping[key_from_graph]
                            else:
                                key = key_from_graph
                        else:
                            key = key_from_graph
                        value = item["value"]
                        metrics[key] = value

                    self.metrics = metrics
                    return self.metrics

                else:
                    raise Exception("Can not retrieve data without Corpus URI. Set attribute uri first")
            else:
                raise Exception("Can not retrieve metrics without database connection.")

    def get_id(self) -> str:
        """Get id of a corpus.

        Uses SPARQL query "CorpusId" of the module "sparql_queries".

        """
        if self.id:
            return self.id
        else:
            if self.database:
                if self.uri:
                    query = CorpusId()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    if len(results) > 0:
                        self.id = results[0]
                        return self.id
                    else:
                        raise Exception("No ID in the knowledge graph.")

                else:
                    raise Exception("URI of corpus is not set.")
            else:
                raise Exception("Can't retrieve ID without database connection.")

    def get_name(self) -> str:
        """Get name of a corpus.

        Uses SPARQL query "CorpusName" of the module "sparql_queries".

        corpus_name as Identifier is a deprecated construct. Should be removed.
        """
        if self.name:
            return self.name
        else:
            if self.database:
                if self.uri:
                    query = CorpusName()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    if len(results) > 0:
                        self.name = results[0]
                        return self.name
                    else:
                        raise Exception("No name in the knowledge graph.")

                else:
                    raise Exception("URI of corpus is not set.")
            else:
                raise Exception("Can't retrieve name without database connection.")

    def get_acronym(self) -> str:
        """Get corpus acronym

        Uses SPARQL query "CorpusAcronym" of the module "sparql_queries".

        """
        if self.acronym:
            return self.acronym
        else:
            if self.database:
                if self.uri:
                    query = CorpusAcronym()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    if len(results) > 0:
                        self.acronym = results[0]
                        return self.acronym
                    else:
                        raise Exception("No acronym in the knowledge graph.")

                else:
                    raise Exception("URI of corpus is not set.")

            else:
                raise Exception("Can't retrieve acronym without database connection.")

    def get_description(self) -> str:
        """Get description of a corpus"""
        if self.description:
            return self.description

    def get_licence(self) -> dict:
        """Get licence of a corpus"""
        if self.licence:
            return self.licence

    def get_repository(self) -> dict:
        """Get repository of a corpus"""
        if self.repository:
            return self.repository

    def get_metadata(self, include_metrics: bool = False, validation: bool = False) -> dict:
        """Serialize Corpus Metadata.

        Args:
            include_metrics (bool, optional): Include metrics. Defaults to False.
            validation (bool, optional): Validate with schema "Corpus".

        Returns:
            dict: Serialization of the corpus metadata.
        """

        metadata = dict(
            id=self.id,
            uri=self.uri,
            corpusName=self.get_name(),
            acronym=self.get_acronym(),
            corpusDescription=self.get_description(),
            licence=self.get_licence()["name"],
            licenceUrl=self.get_licence()["uri"],
            repository=self.get_repository()["url"]
        )

        if include_metrics is True:
            # Use the hardcoded mappings by setting use_mapping to True
            metadata["metrics"] = self.get_metrics(use_mapping=True)

        if validation:
            try:
                schema = CorpusSchema()
                schema.load(metadata)
            except:
                raise Exception("Could not validate metadata!")

        return metadata

    def generate_graph(self) -> Graph:
        """Generate graph data of corpus.

        We use that for creating test data.
        """

        # needed for the prefixes
        golem_query = GolemQuery()
        GD = Namespace(golem_query.get_prefix_uri("gd"))
        CRM = Namespace(golem_query.get_prefix_uri("crm"))
        CLS = Namespace(golem_query.get_prefix_uri("cls"))
        TYPE = Namespace(golem_query.get_prefix_uri("gt"))

        g = Graph()
        # add the prefixes
        for item in golem_query.prefixes:
            g.namespace_manager.bind(item["prefix"], URIRef(item["uri"]))

        # instantiate corpus
        g.add((URIRef(self.uri), RDF.type, CLS.X1_Corpus))

        # id of corpus
        if self.id:
            id_uri = self.uri + "/id"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(id_uri)))

            # Corpus ID as Identifier
            g.add((URIRef(id_uri), RDF.type, CRM.E42_Identifier))
            g.add((URIRef(id_uri), CRM.P2_has_type, TYPE.id))
            g.add((URIRef(id_uri), RDF.value, Literal(self.id)))

        # rdfs label and name as appellation
        if self.name:
            g.add((URIRef(self.uri), RDFS.label, Literal(self.name)))

            name_uri = self.uri + "/corpus_name"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(name_uri)))

            # Corpus name a Appellation...
            g.add((URIRef(name_uri), RDF.type, CRM.E41_Appellation))
            g.add((URIRef(name_uri), CRM.P2_has_type, TYPE.corpus_name))
            g.add((URIRef(name_uri), CRM.P1i_identifies, URIRef(self.uri)))
            g.add((URIRef(name_uri), RDF.value, Literal(self.name)))

        # Acronym
        if self.acronym:
            acronym_uri = self.uri + "/acronym"
            g.add((URIRef(self.uri), CRM.P1_is_identified_by, URIRef(acronym_uri)))

            # Acronym a Appellation...
            g.add((URIRef(URIRef(acronym_uri)), RDF.type, CRM.E41_Appellation))
            g.add((URIRef(acronym_uri), CRM.P1i_identifies, URIRef(self.uri)))
            g.add((URIRef(acronym_uri), RDF.value, Literal(self.acronym)))

        # Description
        if self.description:
            g.add((URIRef(self.uri), CRM.P3_has_note, Literal(self.description)))

        if self.licence:
            right_uri = self.uri + "/licence"
            g.add((URIRef(self.uri), CRM.P104_is_subject_to, URIRef(right_uri)))

            # E30 Right
            # TODO: Check this!
            g.add((URIRef(right_uri), RDF.type, CRM.E30_Right))
            g.add((URIRef(right_uri), CRM.P3_has_note, Literal(self.licence["name"])))
            g.add((URIRef(right_uri), CRM.P67_refers_to, URIRef(self.licence["uri"])))

        if self.metrics:
            for key in self.metrics.keys():
                dim_uri = self.uri + "/dimension/" + key
                g.add((URIRef(self.uri), CRM.P43_has_dimension, URIRef(dim_uri)))

                g.add((URIRef(dim_uri), RDF.type, CRM.E54_Dimension))
                # I assume, they are all integers
                g.add((URIRef(dim_uri), CRM.P90_has_value, Literal(self.metrics[key], datatype=XSD.int)))
                # TODO: add a Unit

        return g

