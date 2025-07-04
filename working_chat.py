"""
Simple Working Chat Interface
Actually finds and shows real data from your database
"""

import os
from simple_working_coordinator import SimpleWorkingCoordinator


def main():
    """Simple working chat."""
    print("🎓 WORKING EDUCATIONAL CHAT")
    print("=" * 50)
    print("I'll search the real database and show you actual content!")
    print("Commands: 'quit', 'debug', 'help'")
    print("=" * 50)

    try:
        coordinator = SimpleWorkingCoordinator()
        print("✅ Ready!")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return

    while True:
        try:
            user_input = input("\n🧑 You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break

            elif user_input.lower() == 'debug':
                print("🐛 Running debug...")
                from debug_search_tools import main as debug_main
                debug_main()
                continue

            elif user_input.lower() == 'help':
                print("""
💡 Try asking:
• "How many courses are there?"
• "List all courses"  
• "Give me 5 blockchain tasks"
• "Find machine learning courses"
• "I want to learn web development"
• "Show me Python resources"
                """)
                continue

            elif not user_input:
                print("🤔 What would you like to learn?")
                continue

            print(f"🔍 Searching database for: '{user_input}'")
            result = coordinator.process_query(user_input)

            print("\n🤖 Assistant:")
            print("-" * 40)
            print(result)
            print("-" * 40)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
