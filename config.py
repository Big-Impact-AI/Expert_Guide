from dotenv import load_dotenv
import os
load_dotenv()
# Configuration file for the educational RAG system

# === SUPABASE CONFIG ===
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
# === OPENAI CONFIG ===
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_DIM = 1536

# === AGENT CONFIG ===
DEFAULT_SIMILARITY_THRESHOLD = 0.7
DEFAULT_SEARCH_LIMIT = 5
MAX_SEARCH_LIMIT = 10

# === QUERY CLASSIFICATION KEYWORDS ===
COURSE_KEYWORDS = [
    'course', 'curriculum', 'program', 'class', 'training', 'bootcamp',
    'degree', 'certification', 'education', 'learning path', 'syllabus'
]

TASK_KEYWORDS = [
    'task', 'assignment', 'project', 'homework', 'exercise', 'activity',
    'practice', 'quiz', 'test', 'challenge', 'problem', 'work'
]

RESOURCE_KEYWORDS = [
    'resource', 'material', 'reference', 'link', 'article', 'documentation',
    'guide', 'tutorial', 'book', 'video', 'tool', 'website', 'library'
]

GENERAL_KEYWORDS = [
    'learn', 'study', 'understand', 'explore', 'research', 'find',
    'discover', 'help', 'explain', 'teach', 'knowledge', 'information'
]