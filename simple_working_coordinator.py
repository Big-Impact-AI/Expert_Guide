from crewai import Crew, Process, Task
from agents.educational_assistant import create_educational_assistant
from tools.database_query_tool import database_query_tool
import json


class SimpleWorkingCoordinator:
    """Simple coordinator that actually works and finds real data."""

    def __init__(self):
        self.assistant = create_educational_assistant()

    def process_query(self, user_query: str) -> str:
        """Process user query and return helpful response."""

        # Handle simple informational queries directly
        query_lower = user_query.lower()

        if any(phrase in query_lower for phrase in ['how many courses', 'count courses']):
            try:
                result = database_query_tool._run('count_all')
                data = json.loads(result)
                return f"📊 We have **{data['total_courses']} courses**, {data['total_tasks']} tasks, and {data['total_resources']} resources in our database."
            except Exception as e:
                return f"I had trouble checking the database: {e}"

        elif any(phrase in query_lower for phrase in ['list courses', 'show courses', 'all courses']):
            try:
                result = database_query_tool._run('list_courses', limit=10)
                data = json.loads(result)
                response = f"📚 **Our {data['total_courses']} courses:**\n\n"
                for i, course in enumerate(data['courses'], 1):
                    response += f"{i}. **{course['title']}**\n   {course['description'][:100]}...\n\n"
                return response
            except Exception as e:
                return f"I had trouble listing courses: {e}"

        # For all other queries, create a simple task for the assistant
        task = Task(
            description=f"""
            The user asked: "{user_query}"

            Your job is to help them by searching our educational database.

            STEP BY STEP:
            1. Look at what they're asking for (tasks, courses, resources, plans)
            2. Use the appropriate search tool to find real content
            3. Present what you actually find in the database
            4. If they want a specific number of items, try to provide that many
            5. If they mention a timeframe, organize accordingly

            SEARCH STRATEGY:
            - Start with similarity_threshold=0.4
            - If no results, try similarity_threshold=0.2  
            - Use comprehensive_search_tool for broad requests
            - Use specific tools (task_search_tool, course_search_tool, resource_search_tool) for focused requests

            BE HELPFUL AND HONEST:
            - Show actual titles and descriptions from the database
            - If you don't find much, say so and suggest alternatives
            - Always offer to help find more or different content
            """,
            agent=self.assistant,
            expected_output="A helpful response with actual database content that addresses the user's specific request"
        )

        # Execute the task
        crew = Crew(
            agents=[self.assistant],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )

        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"I encountered an issue: {e}. Let me try a different approach - what specific topic are you interested in?"


def main():
    """Test the coordinator."""
    coordinator = SimpleWorkingCoordinator()

    test_queries = [
        "How many courses are there?",
        "List all courses",
        "Give me 5 blockchain tasks",
        "I want to learn machine learning",
        "Find web development resources"
    ]

    for query in test_queries:
        print(f"\n🔤 Testing: {query}")
        print("-" * 40)
        result = coordinator.process_query(query)
        print(result)
        print("=" * 60)


if __name__ == "__main__":
    main()