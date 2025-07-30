import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .database import create_tables, database
from .graphql_app import schema

# Create FastAPI app
app = FastAPI(title="FastAPI + GraphQL Demo", version="1.0.0")

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup():
    create_tables()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {
        "message": "FastAPI + GraphQL Demo",
        "graphql_endpoint": "/graphql",
        "graphql_playground": "/graphql (GraphiQL interface)",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
