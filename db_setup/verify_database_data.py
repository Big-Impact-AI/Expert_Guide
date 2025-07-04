"""
Script to verify the dummy data in the database and test the search functions.
"""
from supabase import create_client
import openai
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


def check_data_counts():
    """Check the count of records in each table."""
    print("📊 Checking data counts...")

    tables = ['courses', 'tasks', 'resources']
    total_records = 0

    for table in tables:
        try:
            result = supabase.table(table).select("id", count="exact").execute()
            count = result.count
            total_records += count
            print(f"  {table.capitalize()}: {count} records")
        except Exception as e:
            print(f"  ❌ Error checking {table}: {e}")

    print(f"  Total records: {total_records}")
    return total_records > 0


def show_sample_data():
    """Show sample data from each table."""
    print("\n📋 Sample data from each table:")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        print(f"\n{table.upper()}:")
        try:
            result = supabase.table(table).select("*").limit(3).execute()
            for i, record in enumerate(result.data, 1):
                title = record.get('title', 'No title')
                print(f"  {i}. {title}")
        except Exception as e:
            print(f"  ❌ Error fetching {table}: {e}")


def test_search_functions():
    """Test the vector search functions."""
    print("\n🔍 Testing vector search functions...")

    # Test queries for each domain
    test_queries = [
        ("Python machine learning", "courses"),
        ("JavaScript exercises", "tasks"),
        ("blockchain tutorials", "resources")
    ]

    for query, expected_type in test_queries:
        print(f"\n🔎 Testing query: '{query}' (expecting {expected_type})")

        try:
            # Generate embedding
            query_embedding = embed_query(query)
            if not query_embedding:
                print("  ❌ Failed to generate embedding")
                continue

            # Test course search
            course_result = supabase.rpc('match_courses', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,  # Low threshold for testing
                'match_count': 3
            }).execute()

            print(f"  📚 Found {len(course_result.data)} courses")
            for course in course_result.data[:2]:
                print(f"    - {course['title']} (similarity: {course['similarity']:.3f})")

            # Test task search
            task_result = supabase.rpc('match_tasks', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,
                'match_count': 3,
                'course_filter': None
            }).execute()

            print(f"  📝 Found {len(task_result.data)} tasks")
            for task in task_result.data[:2]:
                print(f"    - {task['title']} (similarity: {task['similarity']:.3f})")

            # Test resource search
            resource_result = supabase.rpc('match_resources', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,
                'match_count': 3,
                'course_filter': None
            }).execute()

            print(f"  📚 Found {len(resource_result.data)} resources")
            for resource in resource_result.data[:2]:
                print(f"    - {resource['title']} (similarity: {resource['similarity']:.3f})")

        except Exception as e:
            print(f"  ❌ Search failed: {e}")


def test_comprehensive_search():
    """Test the comprehensive search functionality."""
    print("\n🌐 Testing comprehensive search...")

    test_query = "machine learning basics"
    print(f"Query: '{test_query}'")

    try:
        query_embedding = embed_query(test_query)
        if not query_embedding:
            print("❌ Failed to generate embedding")
            return

        # Simulate comprehensive search
        results = {}

        # Search courses
        course_result = supabase.rpc('match_courses', {
            'query_embedding': query_embedding,
            'match_threshold': 0.3,
            'match_count': 3
        }).execute()
        results['courses'] = course_result.data

        # Search tasks
        task_result = supabase.rpc('match_tasks', {
            'query_embedding': query_embedding,
            'match_threshold': 0.3,
            'match_count': 3,
            'course_filter': None
        }).execute()
        results['tasks'] = task_result.data

        # Search resources
        resource_result = supabase.rpc('match_resources', {
            'query_embedding': query_embedding,
            'match_threshold': 0.3,
            'match_count': 3,
            'course_filter': None
        }).execute()
        results['resources'] = resource_result.data

        total_results = len(results['courses']) + len(results['tasks']) + len(results['resources'])
        print(f"✅ Comprehensive search found {total_results} total results:")
        print(f"  - {len(results['courses'])} courses")
        print(f"  - {len(results['tasks'])} tasks")
        print(f"  - {len(results['resources'])} resources")

        # Show top result from each category
        if results['courses']:
            top_course = results['courses'][0]
            print(f"\n📚 Top course: {top_course['title']}")

        if results['tasks']:
            top_task = results['tasks'][0]
            print(f"📝 Top task: {top_task['title']}")

        if results['resources']:
            top_resource = results['resources'][0]
            print(f"🔗 Top resource: {top_resource['title']}")

    except Exception as e:
        print(f"❌ Comprehensive search failed: {e}")


def check_embedding_quality():
    """Check if embeddings are properly stored."""
    print("\n🧮 Checking embedding quality...")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        try:
            result = supabase.table(table).select("embedding").limit(1).execute()
            if result.data and result.data[0].get('embedding'):
                embedding = result.data[0]['embedding']
                if isinstance(embedding, list) and len(embedding) == 1536:
                    print(f"  ✅ {table}: Embeddings properly formatted (vector of {len(embedding)})")
                else:
                    print(f"  ⚠️ {table}: Embedding format issue - type: {type(embedding)}")
            else:
                print(f"  ❌ {table}: No embeddings found")
        except Exception as e:
            print(f"  ❌ {table}: Error checking embeddings - {e}")


def main():
    """Main verification function."""
    print("🔍 Database Data Verification")
    print("=" * 50)

    # Check if we have data
    has_data = check_data_counts()

    if not has_data:
        print("\n❌ No data found in database!")
        print("💡 Run the dummy data seeder script first:")
        print("   python comprehensive_dummy_data_seeder.py")
        return

    # Show sample data
    show_sample_data()

    # Check embedding quality
    check_embedding_quality()

    # Test search functions
    test_search_functions()

    # Test comprehensive search
    test_comprehensive_search()

    print("\n" + "=" * 50)
    print("✅ Verification completed!")
    print("\n💡 If searches are working, you can now test the CrewAI system:")
    print("   python example_usage.py")


if __name__ == "__main__":
    main()