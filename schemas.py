from marshmallow import Schema, fields, validate


class ApiInfoSchema(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    name = fields.Str()
    version = fields.Str()
    description = fields.Str()


class CorpusMetricsSchema(Schema):
    """Schema of the corpus metrics included in the corpus metadata"""
    documents = fields.Int(required=False)
    chapters = fields.Int(required=False)
    paragraphs = fields.Int(required=False)
    characters = fields.Int(required=False)
    male = fields.Int(required=False)
    female = fields.Int(required=False)
    nonbinary = fields.Int(required=False)
    comments = fields.Int(required=False)
    wordsInDocuments = fields.Int(required=False)
    wordsInComments = fields.Int(required=False)


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
    uri = fields.Str()
    characterType = fields.Str(validate=validate.OneOf(["canon", "fanon"]))
    characterName = fields.Str()
    characterGender = fields.Str(validate=validate.OneOf(["male", "female", "nonbinary"]))
    entryName = fields.Str()
    refs = fields.Nested(ExternalReferenceSchema, required=False)
    sourceName = fields.Str()
    sourceUrl = fields.Str()
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
