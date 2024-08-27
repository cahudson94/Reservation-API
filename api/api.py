"""."""
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from api.schemas.mutation_schema import Mutation
from api.schemas.query_schema import Query

schema = strawberry.Schema(query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=True))

def create_api():
    """."""
    api = FastAPI()
    router = GraphQLRouter(schema)
    api.include_router(router, prefix="/graphql")

    return api
