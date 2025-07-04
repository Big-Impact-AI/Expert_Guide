"""
Setup verification script to check if database tables and functions are created correctly.
Run this after executing the SQL setup script.
"""
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def check_tables_exist():
    """Check if all required tables exist."""
    print("🔍 Checking if tables exist...")

    required_tables = ['courses', 'tasks', 'resources']

    try:
        # Try to query each table
        for table in required_tables:
            result = supabase.table(table).select("count", count="exact").execute()
            print(f"  ✅ Table '{table}' exists (currently has {result.count} records)")

        return True

    except Exception as e:
        print(f"  ❌ Error checking tables: {e}")
        return False


def check_functions_exist():
    """Check if vector search functions exist."""
    print("\n🔧 Checking if search functions exist...")

    functions = ['match_courses', 'match_tasks', 'match_resources']

    for func in functions:
        try:
            # Try to call the function with dummy parameters
            # This will fail gracefully if the function doesn't exist
            result = supabase.rpc(func, {
                'query_embedding': [0.0] * 1536,  # Dummy embedding
                'match_threshold': 0.9,  # High threshold so no results
                'match_count': 1
            }).execute()

            print(f"  ✅ Function '{func}' exists and callable")

        except Exception as e:
            if "Could not find the function" in str(e):
                print(f"  ❌ Function '{func}' does not exist")
            else:
                print(f"  ⚠️ Function '{func}' exists but error: {e}")


def check_vector_extension():
    """Check if vector extension is installed."""
    print("\n🔌 Checking vector extension...")

    try:
        result = supabase.rpc('check_vector_extension').execute()
        print(f"  {result.data}")
    except Exception as e:
        print(f"  ❌ Could not check vector extension: {e}")


def check_table_structure():
    """Check the structure of our tables."""
    print("\n📋 Checking table structures...")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        print(f"\n  📊 {table.upper()} table structure:")
        try:
            result = supabase.rpc('get_table_info', {'table_name': table}).execute()
            for column in result.data:
                print(
                    f"    - {column['column_name']}: {column['data_type']} ({'NULL' if column['is_nullable'] == 'YES' else 'NOT NULL'})")
        except Exception as e:
            print(f"    ❌ Could not get structure: {e}")


def get_record_counts():
    """Get current record counts."""
    print("\n📊 Current record counts...")

    try:
        result = supabase.rpc('get_record_counts').execute()
        for row in result.data:
            print(f"  📈 {row['table_name']}: {row['record_count']} records")
    except Exception as e:
        print(f"  ❌ Could not get counts: {e}")


def test_basic_operations():
    """Test basic database operations."""
    print("\n🧪 Testing basic operations...")

    # Test inserting a simple record (we'll delete it after)
    try:
        test_course = {
            "title": "Test Course",
            "description": "This is a test course for verification",
            "embedding": [0.1] * 1536  # Dummy embedding
        }

        # Insert test record
        result = supabase.table("courses").insert(test_course).execute()
        if result.data:
            course_id = result.data[0]['id']
            print(f"  ✅ Successfully inserted test course (ID: {course_id})")

            # Try to read it back
            read_result = supabase.table("courses").select("*").eq("id", course_id).execute()
            if read_result.data:
                print(f"  ✅ Successfully read back test course")

                # Delete the test record
                delete_result = supabase.table("courses").delete().eq("id", course_id).execute()
                print(f"  ✅ Successfully deleted test course")
            else:
                print(f"  ❌ Could not read back test course")
        else:
            print(f"  ❌ Could not insert test course")

    except Exception as e:
        print(f"  ❌ Basic operations test failed: {e}")


def main():
    """Main verification function."""
    print("🔍 Database Setup Verification")
    print("=" * 50)

    # Check if tables exist
    tables_ok = check_tables_exist()

    if not tables_ok:
        print("\n❌ Tables are missing!")
        print("💡 Run the complete SQL setup script in your Supabase SQL Editor:")
        print("   Copy and paste the 'Complete Database Setup - Tables and Functions' SQL")
        return

    # Check functions
    check_functions_exist()

    # Check vector extension
    check_vector_extension()

    # Check table structures
    check_table_structure()

    # Get current counts
    get_record_counts()

    # Test basic operations
    test_basic_operations()

    print("\n" + "=" * 50)
    print("✅ Setup verification completed!")
    print("\n💡 Next steps:")
    print("1. If everything looks good, run the data seeder:")
    print("   python comprehensive_dummy_data_seeder.py")
    print("2. Then test the CrewAI system:")
    print("   python example_usage.py")


if __name__ == "__main__":
    main()