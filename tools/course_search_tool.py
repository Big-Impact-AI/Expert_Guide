from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from supabase import create_client
import openai
import json
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, EMBEDDING_MODEL

# Initialize clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_query(text: str):
    """Generate embedding for search query."""
    try:
        response = openai_client.embeddings.create(
            input=[text],
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding failed: {e}")
        return []


class CourseSearchInput(BaseModel):
    query: str = Field(..., description="Search query for finding relevant courses")
    limit: int = Field(default=5, description="Number of courses to return (max 20)")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity threshold (0-1)")


class CourseSearchTool(BaseTool):
    name: str = "course_search"
    description: str = "Search for relevant courses based on semantic similarity to your query. Use this when you need to find courses related to specific topics or subjects."
    args_schema: Type[BaseModel] = CourseSearchInput

    def _run(self, query: str, limit: int = 5, similarity_threshold: float = 0.7) -> str:
        try:
            # Generate embedding for the query
            query_embedding = embed_query(query)
            if not query_embedding:
                return "Failed to generate embedding for query"

            # Perform similarity search
            result = supabase.rpc('match_courses', {
                'query_embedding': query_embedding,
                'match_threshold': similarity_threshold,
                'match_count': min(limit, 20)
            }).execute()

            if not result.data:
                return f"No courses found for query: '{query}'"

            # Format results
            courses = []
            for course in result.data:
                courses.append({
                    'id': course['id'],
                    'title': course['title'],
                    'description': course['description'],
                    'similarity': round(course['similarity'], 3)
                })

            return json.dumps(courses, indent=2)

        except Exception as e:
            return f"Error searching courses: {str(e)}"


# Export tool instance
course_search_tool = CourseSearchTool()