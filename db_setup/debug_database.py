"""
Debug script to check database structure and test functions
"""
from supabase import create_client
import openai
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, EMBEDDING_MODEL

# Initialize clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def check_database_structure():
    """Check the structure of our tables."""
    print("🔍 Checking database structure...")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        print(f"\n📋 Table: {table}")
        try:
            # Get table structure
            result = supabase.rpc('get_table_info', {'table_name': table}).execute()
            print(f"Structure check result: {result}")
        except Exception as e:
            print(f"Could not get structure info: {e}")

        # Try to get sample data
        try:
            result = supabase.table(table).select("*").limit(1).execute()
            if result.data:
                print(f"Sample row: {result.data[0]}")
                # Check if embedding column exists and its type
                if 'embedding' in result.data[0]:
                    embedding = result.data[0]['embedding']
                    print(f"Embedding type: {type(embedding)}")
                    print(f"Embedding sample: {str(embedding)[:100]}...")
                else:
                    print("❌ No embedding column found!")
            else:
                print("⚠️ No data in table")
        except Exception as e:
            print(f"Error getting sample data: {e}")


def test_functions():
    """Test if our vector search functions work."""
    print("\n🧪 Testing vector search functions...")

    # Generate a test embedding
    try:
        response = openai_client.embeddings.create(
            input=["test query"],
            model=EMBEDDING_MODEL
        )
        test_embedding = response.data[0].embedding
        print(f"✅ Generated test embedding of length: {len(test_embedding)}")
    except Exception as e:
        print(f"❌ Failed to generate test embedding: {e}")
        return

    # Test each function
    functions = [
        ('match_courses', {'query_embedding': test_embedding, 'match_threshold': 0.1, 'match_count': 5}),
        ('match_tasks',
         {'query_embedding': test_embedding, 'match_threshold': 0.1, 'match_count': 5, 'course_filter': None}),
        ('match_resources',
         {'query_embedding': test_embedding, 'match_threshold': 0.1, 'match_count': 5, 'course_filter': None})
    ]

    for func_name, params in functions:
        print(f"\n🔧 Testing {func_name}...")
        try:
            result = supabase.rpc(func_name, params).execute()
            print(f"✅ {func_name} works! Found {len(result.data)} results")
            if result.data:
                print(f"Sample result: {result.data[0]}")
        except Exception as e:
            print(f"❌ {func_name} failed: {e}")


def check_vector_extension():
    """Check if vector extension is installed."""
    print("\n🔌 Checking vector extension...")
    try:
        result = supabase.rpc('check_vector_extension').execute()
        print(f"Vector extension check: {result}")
    except Exception as e:
        print(f"Could not check vector extension: {e}")


def create_test_function():
    """Create a simple test function to check SQL execution."""
    print("\n⚡ Creating test function...")
    try:
        # This should work if we can execute SQL
        result = supabase.rpc('test_simple_function').execute()
        print(f"Test function result: {result}")
    except Exception as e:
        print(f"Test function failed: {e}")


def count_records():
    """Count records in each table."""
    print("\n📊 Counting records...")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        try:
            result = supabase.table(table).select("id", count="exact").execute()
            count = result.count
            print(f"📈 {table}: {count} records")
        except Exception as e:
            print(f"❌ Error counting {table}: {e}")


def main():
    """Run all debug checks."""
    print("🔧 Database Debug Script")
    print("=" * 50)

    count_records()
    check_database_structure()
    test_functions()

    print("\n" + "=" * 50)
    print("💡 If functions are missing, run the SQL from 'Fixed Supabase Vector Search Functions'")
    print("💡 If tables are empty, run the data seeding script first")


if __name__ == "__main__":
    main()