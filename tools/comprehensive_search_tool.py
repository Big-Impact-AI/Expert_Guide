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


class ComprehensiveSearchInput(BaseModel):
    query: str = Field(..., description="Search query for finding relevant content across all tables")
    limit_per_table: int = Field(default=3, description="Number of results per table (max 10)")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity threshold (0-1)")


class ComprehensiveSearchTool(BaseTool):
    name: str = "comprehensive_search"
    description: str = "Search across all tables (courses, tasks, resources) simultaneously to get a comprehensive view of relevant content. Use this for broad queries or when you need context from multiple sources."
    args_schema: Type[BaseModel] = ComprehensiveSearchInput

    def _run(self, query: str, limit_per_table: int = 3, similarity_threshold: float = 0.7) -> str:
        try:
            # Generate embedding for the query
            query_embedding = embed_query(query)
            if not query_embedding:
                return "Failed to generate embedding for query"

            results = {}
            limit = min(limit_per_table, 10)

            # Search courses
            try:
                course_result = supabase.rpc('match_courses', {
                    'query_embedding': query_embedding,
                    'match_threshold': similarity_threshold,
                    'match_count': limit
                }).execute()
                results['courses'] = course_result.data or []
            except Exception as e:
                results['courses'] = []
                print(f"Course search failed: {e}")

            # Search tasks
            try:
                task_result = supabase.rpc('match_tasks', {
                    'query_embedding': query_embedding,
                    'match_threshold': similarity_threshold,
                    'match_count': limit,
                    'course_filter': None
                }).execute()
                results['tasks'] = task_result.data or []
            except Exception as e:
                results['tasks'] = []
                print(f"Task search failed: {e}")

            # Search resources
            try:
                resource_result = supabase.rpc('match_resources', {
                    'query_embedding': query_embedding,
                    'match_threshold': similarity_threshold,
                    'match_count': limit,
                    'course_filter': None
                }).execute()
                results['resources'] = resource_result.data or []
            except Exception as e:
                results['resources'] = []
                print(f"Resource search failed: {e}")

            # Format comprehensive results
            formatted_results = {
                'query': query,
                'total_results': len(results['courses']) + len(results['tasks']) + len(results['resources']),
                'courses': [
                    {
                        'id': c['id'],
                        'title': c['title'],
                        'description': c['description'][:200] + '...' if len(c['description']) > 200 else c[
                            'description'],
                        'similarity': round(c['similarity'], 3)
                    } for c in results['courses']
                ],
                'tasks': [
                    {
                        'id': t['id'],
                        'title': t['title'],
                        'content': t['content'][:200] + '...' if len(t['content']) > 200 else t['content'],
                        'course_id': t['course_id'],
                        'similarity': round(t['similarity'], 3)
                    } for t in results['tasks']
                ],
                'resources': [
                    {
                        'id': r['id'],
                        'title': r['title'],
                        'url': r['url'],
                        'tags': r['tags'],
                        'course_id': r['course_id'],
                        'similarity': round(r['similarity'], 3)
                    } for r in results['resources']
                ]
            }

            return json.dumps(formatted_results, indent=2)

        except Exception as e:
            return f"Error in comprehensive search: {str(e)}"


# Export tool instance
comprehensive_search_tool = ComprehensiveSearchTool()