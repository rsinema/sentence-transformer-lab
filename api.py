from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from srv.ebook_services import query_database

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str
    num_results: int = 5
    books: bool = False

class SearchResult(BaseModel):
    title: str
    text: str
    similarity: float

# Replace this with your actual vector database interaction code
async def query_vector_db(text: str, num_results: int, books: bool) -> List[SearchResult]:
    # Add your vector database query logic here
    # Example return format:
    return query_database(text, num_results, False, books)


@app.post("/api/search", response_model=List[SearchResult])
async def search(query: Query):
    results = await query_vector_db(query.text, query.num_results, query.books)
    return results