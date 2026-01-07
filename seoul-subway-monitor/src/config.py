import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SEOUL_API_KEY = os.getenv("SEOUL_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validation
if not SEOUL_API_KEY:
    print("Warning: SEOUL_API_KEY is not set in .env")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: Supabase credentials are not set in .env")
