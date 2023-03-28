from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


class ApiInfo(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    name = fields.Str()
    version = fields.Str()
    description = fields.Str()


class CorpusMetrics(Schema):
    """Schema of the corpus metrics included in the corpus metadata"""
    poems = fields.Int()
    authors = fields.Int()
    stanzas = fields.Int()
    verses = fields.Int()
    words = fields.Int()
    grammaticalSyllables = fields.Int()
    metricalSyllables = fields.Int()


class CorpusMetadata(Schema):
    name = fields.Str()
    title = fields.Str()
    description = fields.Str()
    metrics = fields.Nested(CorpusMetrics, required=False)


class AuthorMetadata(Schema):
    name = fields.Str()
    uri = fields.Str()


class PoemAnalysisSource(Schema):
    uri = fields.Str()


class PoemAnalysis(Schema):
    source = fields.Nested(PoemAnalysisSource)
    numOfStanzas = fields.Int()
    numOfLines = fields.Int()
    numOfWords = fields.Int()
    numOfLinesInStanzas = fields.List(fields.Int())
    rhymeSchemesOfStanzas = fields.List(fields.Str())
    numOfMetricalSyllables = fields.Int()
    numOfGrammaticalSyllables = fields.Int()
    numOfMetricalSyllablesInStanzas = fields.List(fields.List(fields.Int()))
    numOfGrammaticalSyllablesInStanzas = fields.List(fields.List(fields.Int()))
    numOfWordsInStanzas = fields.List(fields.List(fields.Int()))
    grammaticalStressPatternsInStanzas = fields.List(fields.List(fields.Str()))
    metricalPatternsInStanzas = fields.List(fields.List(fields.Str()))


class PoemMetadata(Schema):
    id = fields.Str()
    uri = fields.Str()
    name = fields.Str()
    source = fields.Str()
    sourceUri = fields.Str()
    authors = fields.List(fields.Nested(AuthorMetadata), required=False)
    analysis = fields.Nested(PoemAnalysis, required=False)


spec = APISpec(
    title="Poecor POSTDATA connector",
    version="1.0",
    openapi_version="3.0.3",
    info=dict(
        description="""
Middleware to connect POSTDATA to a DraCor-like frontend.""",
        contact=dict(
            name="Ingo Börner",
            email="ingo.boerner@uni-potsdam.de"
        ),
        license=dict(
            name="GPL-3.0 license",
            url="https://www.gnu.org/licenses/gpl-3.0.html"
        )
    ),
    servers=[
        dict(
            description="Local Flask",
            url="http://localhost:5000"
        ),
        dict(
            description="Production",
            url="https://poecor.org/api"
        ),
        dict(
            description="Staging",
            url="https://staging.poecor.org/api"
        )
    ],
    externalDocs=dict(
        description="Code on Github",
        url="https://github.com/dh-network/postdata-2-dracor-api"
    ),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)
