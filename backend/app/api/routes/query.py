from fastapi import APIRouter

from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.services.retrieval import retrieve_documents, build_context
from backend.app.services.generation import generate_answer

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    results = retrieve_documents(request.question, top_k=3)

    context = build_context(results)

    answer = generate_answer(
        request.question,
        context,
    )

    sources = []

    for metadata in results["metadatas"][0]:
        source = metadata["source"]
        if source not in sources:
            sources.append(source)

    return QueryResponse(
        answer=answer,
        sources=sources,
    )
