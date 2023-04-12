from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


spec = APISpec(
    title="GOLEM DraCor frontend connector",
    version="1.0",
    openapi_version="3.0.3",
    info=dict(
        description="""
Middleware to connect GOLEM's Triple Store to a DraCor-like frontend.""",
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
        )
    ],
    externalDocs=dict(
        description="Code on Github",
        url="https://github.com/ingoboerner/golem-dracor-frontend-api"
    ),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)
