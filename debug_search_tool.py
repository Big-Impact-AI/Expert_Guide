"""
Debug script to test the search tools and see what's actually in the database
"""
from tools.task_search_tool import task_search_tool
from tools.course_search_tool import course_search_tool
from tools.resource_search_tool import resource_search_tool
from tools.comprehensive_search_tool import comprehensive_search_tool
from tools.database_query_tool import database_query_tool
import json


def test_direct_database_access():
    """Test direct database queries first."""
    print("🔍 Testing direct database access...")

    try:
        # Test count query
        result = database_query_tool._run('count_all')
        print(f"Count result: {result}")

        # Test list courses
        result = database_query_tool._run('list_courses', limit=5)
        print(f"Courses list: {result}")

    except Exception as e:
        print(f"❌ Database query failed: {e}")


def test_search_tools():
    """Test all search tools with different queries."""
    print("\n🔍 Testing search tools...")

    test_queries = [
        "blockchain",
        "machine learning",
        "web development",
        "python",
        "javascript"
    ]

    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")

        # Test task search
        try:
            print("📝 Task search:")
            result = task_search_tool._run(query, limit=3, similarity_threshold=0.3)
            print(f"Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Task search failed: {e}")

        # Test course search
        try:
            print("📚 Course search:")
            result = course_search_tool._run(query, limit=3, similarity_threshold=0.3)
            print(f"Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Course search failed: {e}")

        # Test resource search
        try:
            print("🔗 Resource search:")
            result = resource_search_tool._run(query, limit=3, similarity_threshold=0.3)
            print(f"Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Resource search failed: {e}")


def test_comprehensive_search():
    """Test comprehensive search specifically."""
    print("\n🌐 Testing comprehensive search...")

    queries = ["blockchain", "machine learning", "programming"]

    for query in queries:
        print(f"\n--- Comprehensive search for: '{query}' ---")
        try:
            result = comprehensive_search_tool._run(
                query=query,
                limit_per_table=3,
                similarity_threshold=0.3
            )

            # Parse and display results
            data = json.loads(result)
            print(f"Total results: {data['total_results']}")
            print(f"Courses found: {len(data['courses'])}")
            print(f"Tasks found: {len(data['tasks'])}")
            print(f"Resources found: {len(data['resources'])}")

            if data['courses']:
                print("Sample course:", data['courses'][0]['title'])
            if data['tasks']:
                print("Sample task:", data['tasks'][0]['title'])
            if data['resources']:
                print("Sample resource:", data['resources'][0]['title'])

        except Exception as e:
            print(f"❌ Comprehensive search failed: {e}")


def test_with_lower_thresholds():
    """Test with very low similarity thresholds to see if we get any results."""
    print("\n🔬 Testing with very low similarity thresholds...")

    try:
        result = task_search_tool._run(
            "blockchain",
            limit=10,
            similarity_threshold=0.1  # Very low threshold
        )
        print("Low threshold task search result:")
        print(result)

    except Exception as e:
        print(f"❌ Low threshold search failed: {e}")


def check_actual_database_content():
    """Check what's actually in the database tables."""
    print("\n📊 Checking actual database content...")

    from supabase import create_client
    from config import SUPABASE_URL, SUPABASE_KEY

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        try:
            # Get count
            count_result = supabase.table(table).select("id", count="exact").execute()
            print(f"\n{table.upper()}: {count_result.count} records")

            # Get sample records
            sample_result = supabase.table(table).select("id, title").limit(3).execute()
            for record in sample_result.data:
                print(f"  - ID {record['id']}: {record['title']}")

        except Exception as e:
            print(f"❌ Error checking {table}: {e}")


def main():
    """Run all debug tests."""
    print("🐛 DEBUGGING SEARCH TOOLS")
    print("=" * 50)

    check_actual_database_content()
    test_direct_database_access()
    test_search_tools()
    test_comprehensive_search()
    test_with_lower_thresholds()

    print("\n" + "=" * 50)
    print("🎯 Debug complete! Check the results above to see what's working.")


if __name__ == "__main__":
    main()