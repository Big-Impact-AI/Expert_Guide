"""
Example usage of the Educational RAG Coordinator system.

This file demonstrates how to use the coordinator to handle different
types of user queries automatically.
"""

from main_coordinator import EducationalRAGCoordinator


def demo_automatic_routing():
    """Demonstrate automatic query routing and processing."""

    coordinator = EducationalRAGCoordinator()

    # Example queries that will be automatically routed
    demo_queries = [
        {
            "query": "I'm a complete beginner and want to learn Python programming",
            "description": "Simple learning request - should route to Educational Assistant"
        },
        {
            "query": "Compare the best machine learning courses available",
            "description": "Comparison request - should route to Course Curator"
        },
        {
            "query": "Find comprehensive resources for data science including tools and references",
            "description": "Resource request - should route to Research Assistant"
        },
        {
            "query": "Create a complete learning roadmap for becoming a full-stack web developer with courses, practice projects, and resources",
            "description": "Complex planning request - should use multiple agents"
        },
        {
            "query": "What are some practical JavaScript exercises I can do?",
            "description": "Task-focused request - should route to Educational Assistant"
        }
    ]

    print("🎓 Educational RAG Coordinator - Automatic Routing Demo")
    print("=" * 70)

    for i, demo in enumerate(demo_queries, 1):
        print(f"\n📝 Demo {i}: {demo['description']}")
        print(f"Query: \"{demo['query']}\"")
        print("-" * 50)

        try:
            # Process the query with full coordination
            result = coordinator.process_user_query(
                demo['query'],
                use_coordinator=True  # Use query coordinator for analysis
            )

            print("✅ Result:")
            print(result)

        except Exception as e:
            print(f"❌ Error processing query: {e}")

        print("\n" + "=" * 70)


def demo_quick_search():
    """Demonstrate quick search functionality for simple queries."""

    coordinator = EducationalRAGCoordinator()

    print("\n🔍 Quick Search Demo")
    print("=" * 50)

    # Quick searches without full crew processing
    quick_searches = [
        ("Python basics", "comprehensive"),
        ("machine learning algorithms", "course"),
        ("data visualization tools", "resource")
    ]

    for query, search_type in quick_searches:
        print(f"\n🔎 Quick {search_type} search: \"{query}\"")
        print("-" * 30)

        try:
            result = coordinator.quick_search(query, search_type)
            print("Results found:")
            print(result[:500] + "..." if len(result) > 500 else result)

        except Exception as e:
            print(f"❌ Error in quick search: {e}")


def interactive_mode():
    """Interactive mode for testing custom queries."""

    coordinator = EducationalRAGCoordinator()

    print("\n🎯 Interactive Mode")
    print("Enter your educational queries (type 'quit' to exit)")
    print("=" * 50)

    while True:
        user_query = input("\n📝 Your query: ").strip()

        if user_query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not user_query:
            print("Please enter a valid query.")
            continue

        print(f"\n🤖 Processing: \"{user_query}\"")
        print("-" * 40)

        try:
            # Show intent analysis first
            intent = coordinator.analyze_query_intent(user_query)
            print(f"🎯 Detected intent: {intent['primary_intent']} ({intent['complexity']} complexity)")

            # Ask user if they want full processing or quick search
            mode = input("\nChoose mode (f=full processing, q=quick search): ").lower()

            if mode == 'q':
                result = coordinator.quick_search(user_query)
                print("\n🔍 Quick search results:")
            else:
                result = coordinator.process_user_query(user_query, use_coordinator=False)
                print("\n✅ Full processing results:")

            print(result)

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function with different demo modes."""

    print("🎓 Educational RAG System Demo")
    print("=" * 50)
    print("Choose a demo mode:")
    print("1. Automatic Routing Demo")
    print("2. Quick Search Demo")
    print("3. Interactive Mode")
    print("4. Run All Demos")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == '1':
        demo_automatic_routing()
    elif choice == '2':
        demo_quick_search()
    elif choice == '3':
        interactive_mode()
    elif choice == '4':
        demo_automatic_routing()
        demo_quick_search()
        interactive_mode()
    else:
        print("Invalid choice. Running automatic routing demo...")
        demo_automatic_routing()


if __name__ == "__main__":
    main()