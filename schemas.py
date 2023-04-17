from marshmallow import Schema, fields


class ApiInfoSchema(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    name = fields.Str()
    version = fields.Str()
    description = fields.Str()


class WordCountSchema(Schema):
    """Schema of the wordcount included in CorpusMetrics"""
    wordsInDocuments = fields.Int()
    wordsInComments = fields.Int()


class CorpusMetricsSchema(Schema):
    """Schema of the corpus metrics included in the corpus metadata"""
    documents = fields.Int()
    chapters = fields.Int()
    paragraphs = fields.Int()
    characters = fields.Int()
    male = fields.Int()
    female = fields.Int()
    nonbinary = fields.Int()
    comments = fields.Int()
    wordcount = fields.Nested(WordCountSchema, required=True)


class ExternalReferenceSchema(Schema):
    """Item in External Reference Ressource"""
    ref = fields.Str()
    type = fields.Str()


class AuthorSchema(Schema):
    """Metadata on a single author"""
    id = fields.Str()
    uri = fields.Str() # maybe should add that
    authorName = fields.Str()
    refs = fields.Nested(ExternalReferenceSchema)


class CharacterSchema(Schema):
    """Metadata on a single character"""
    id = fields.Str()
    uri = fields.Str() # would add that
    characterName = fields.Str()
    entryName = fields.Str()
    refs = fields.Nested(ExternalReferenceSchema, required=False)
    sourceName = fields.Str()
    sourceUrl = fields.Str
    createdYear = fields.Int()
    firstFanficYear = fields.Int()
    numDocuments = fields.Int()
    characterCsvUrl = fields.Str()
    authors = fields.Nested(AuthorSchema)


class CorpusSchema(Schema):
    """Schema of the corpus.
    """
    id = fields.Str()
    uri = fields.Str()
    corpusName = fields.Str()
    acronym = fields.Str()
    corpusDescription = fields.Str(required=False)
    licence = fields.Str()
    licenceUrl = fields.Str()
    repository = fields.Str(required=False)
    metrics = fields.Nested(CorpusMetricsSchema, required=False)
    characters = fields.Nested(CharacterSchema, required=False)
