from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
from supabase import create_client
import json
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseQueryInput(BaseModel):
    query_type: str = Field(...,
                            description="Type of query: 'count_all', 'list_courses', 'list_by_course', 'course_details', 'stats'")
    course_id: Optional[int] = Field(default=None, description="Course ID for specific queries")
    limit: int = Field(default=50, description="Limit for list queries")


class DatabaseQueryTool(BaseTool):
    name: str = "database_query"
    description: str = """Direct database query tool for getting factual information about available courses, tasks, and resources. 
    Use this for queries like 'how many courses', 'list all courses', 'what courses are available', 'show me course details'.

    Query types:
    - 'count_all': Get counts of all courses, tasks, and resources
    - 'list_courses': Get list of all available courses
    - 'list_by_course': Get tasks and resources for a specific course
    - 'course_details': Get detailed info about a specific course
    - 'stats': Get comprehensive statistics about the database
    """
    args_schema: Type[BaseModel] = DatabaseQueryInput

    def _run(self, query_type: str, course_id: Optional[int] = None, limit: int = 50) -> str:
        try:
            if query_type == "count_all":
                return self._get_counts()

            elif query_type == "list_courses":
                return self._list_courses(limit)

            elif query_type == "list_by_course":
                if course_id is None:
                    return "Error: course_id required for list_by_course query"
                return self._list_by_course(course_id, limit)

            elif query_type == "course_details":
                if course_id is None:
                    return "Error: course_id required for course_details query"
                return self._get_course_details(course_id)

            elif query_type == "stats":
                return self._get_comprehensive_stats()

            else:
                return f"Error: Unknown query_type '{query_type}'. Use: count_all, list_courses, list_by_course, course_details, stats"

        except Exception as e:
            return f"Database query error: {str(e)}"

    def _get_counts(self) -> str:
        """Get counts of all content types."""
        try:
            # Get course count
            courses_result = supabase.table("courses").select("id", count="exact").execute()
            courses_count = courses_result.count

            # Get tasks count
            tasks_result = supabase.table("tasks").select("id", count="exact").execute()
            tasks_count = tasks_result.count

            # Get resources count
            resources_result = supabase.table("resources").select("id", count="exact").execute()
            resources_count = resources_result.count

            result = {
                "total_courses": courses_count,
                "total_tasks": tasks_count,
                "total_resources": resources_count,
                "total_content_items": courses_count + tasks_count + resources_count,
                "summary": f"We have {courses_count} courses, {tasks_count} tasks, and {resources_count} resources available."
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            return f"Error getting counts: {str(e)}"

    def _list_courses(self, limit: int) -> str:
        """Get list of all available courses."""
        try:
            result = supabase.table("courses").select("id, title, description").limit(limit).execute()

            if not result.data:
                return "No courses found in the database."

            courses_list = {
                "total_courses": len(result.data),
                "courses": []
            }

            for course in result.data:
                # Truncate description for readability
                description = course['description']
                if len(description) > 150:
                    description = description[:150] + "..."

                courses_list["courses"].append({
                    "id": course['id'],
                    "title": course['title'],
                    "description": description
                })

            return json.dumps(courses_list, indent=2)

        except Exception as e:
            return f"Error listing courses: {str(e)}"

    def _list_by_course(self, course_id: int, limit: int) -> str:
        """Get tasks and resources for a specific course."""
        try:
            # Get course info
            course_result = supabase.table("courses").select("id, title, description").eq("id", course_id).execute()

            if not course_result.data:
                return f"Course with ID {course_id} not found."

            course = course_result.data[0]

            # Get tasks for this course
            tasks_result = supabase.table("tasks").select("id, title, content").eq("course_id", course_id).limit(
                limit).execute()

            # Get resources for this course
            resources_result = supabase.table("resources").select("id, title, url, tags").eq("course_id",
                                                                                             course_id).limit(
                limit).execute()

            result = {
                "course": {
                    "id": course['id'],
                    "title": course['title'],
                    "description": course['description'][:200] + "..." if len(course['description']) > 200 else course[
                        'description']
                },
                "tasks_count": len(tasks_result.data),
                "resources_count": len(resources_result.data),
                "tasks": [
                    {
                        "id": task['id'],
                        "title": task['title'],
                        "content": task['content'][:100] + "..." if len(task['content']) > 100 else task['content']
                    }
                    for task in tasks_result.data[:10]  # Show first 10
                ],
                "resources": [
                    {
                        "id": resource['id'],
                        "title": resource['title'],
                        "url": resource['url'],
                        "tags": resource['tags']
                    }
                    for resource in resources_result.data[:10]  # Show first 10
                ]
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            return f"Error getting course content: {str(e)}"

    def _get_course_details(self, course_id: int) -> str:
        """Get detailed information about a specific course."""
        try:
            # Get course info
            course_result = supabase.table("courses").select("*").eq("id", course_id).execute()

            if not course_result.data:
                return f"Course with ID {course_id} not found."

            course = course_result.data[0]

            # Get counts for this course
            tasks_count = supabase.table("tasks").select("id", count="exact").eq("course_id", course_id).execute().count
            resources_count = supabase.table("resources").select("id", count="exact").eq("course_id",
                                                                                         course_id).execute().count

            result = {
                "course_details": {
                    "id": course['id'],
                    "title": course['title'],
                    "description": course['description'],
                    "created_at": course.get('created_at'),
                    "updated_at": course.get('updated_at')
                },
                "content_summary": {
                    "total_tasks": tasks_count,
                    "total_resources": resources_count,
                    "total_learning_items": tasks_count + resources_count
                }
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            return f"Error getting course details: {str(e)}"

    def _get_comprehensive_stats(self) -> str:
        """Get comprehensive statistics about the database."""
        try:
            # Get all courses with their content counts
            courses_result = supabase.table("courses").select("id, title").execute()

            stats = {
                "database_overview": {},
                "courses_breakdown": [],
                "content_distribution": {}
            }

            # Overall counts
            total_courses = len(courses_result.data)
            total_tasks = supabase.table("tasks").select("id", count="exact").execute().count
            total_resources = supabase.table("resources").select("id", count="exact").execute().count

            stats["database_overview"] = {
                "total_courses": total_courses,
                "total_tasks": total_tasks,
                "total_resources": total_resources,
                "avg_tasks_per_course": round(total_tasks / total_courses, 1) if total_courses > 0 else 0,
                "avg_resources_per_course": round(total_resources / total_courses, 1) if total_courses > 0 else 0
            }

            # Per-course breakdown
            for course in courses_result.data:
                course_tasks = supabase.table("tasks").select("id", count="exact").eq("course_id",
                                                                                      course['id']).execute().count
                course_resources = supabase.table("resources").select("id", count="exact").eq("course_id", course[
                    'id']).execute().count

                stats["courses_breakdown"].append({
                    "course_id": course['id'],
                    "course_title": course['title'],
                    "tasks": course_tasks,
                    "resources": course_resources,
                    "total_content": course_tasks + course_resources
                })

            return json.dumps(stats, indent=2)

        except Exception as e:
            return f"Error getting comprehensive stats: {str(e)}"


# Export tool instance
database_query_tool = DatabaseQueryTool()