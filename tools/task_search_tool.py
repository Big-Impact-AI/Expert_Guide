from crewai.tools import BaseTool
from typing import Type, Optional
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


class TaskSearchInput(BaseModel):
    query: str = Field(..., description="Search query for finding relevant tasks")
    course_id: Optional[int] = Field(default=None, description="Optional course ID to filter tasks")
    limit: int = Field(default=5, description="Number of tasks to return (max 20)")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity threshold (0-1)")


class TaskSearchTool(BaseTool):
    name: str = "task_search"
    description: str = "Search for relevant tasks based on semantic similarity. Can optionally filter by course ID. Use this when you need to find specific tasks or assignments."
    args_schema: Type[BaseModel] = TaskSearchInput

    def _run(self, query: str, course_id: Optional[int] = None, limit: int = 5,
             similarity_threshold: float = 0.7) -> str:
        try:
            # Generate embedding for the query
            query_embedding = embed_query(query)
            if not query_embedding:
                return "Failed to generate embedding for query"

            # Perform similarity search
            result = supabase.rpc('match_tasks', {
                'query_embedding': query_embedding,
                'match_threshold': similarity_threshold,
                'match_count': min(limit, 20),
                'course_filter': course_id
            }).execute()

            if not result.data:
                return f"No tasks found for query: '{query}'"

            # Format results
            tasks = []
            for task in result.data:
                tasks.append({
                    'id': task['id'],
                    'title': task['title'],
                    'content': task['content'],
                    'course_id': task['course_id'],
                    'similarity': round(task['similarity'], 3)
                })

            return json.dumps(tasks, indent=2)

        except Exception as e:
            return f"Error searching tasks: {str(e)}"


# Export tool instance
task_search_tool = TaskSearchTool()