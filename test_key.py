import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv("kasparoo/.env")

api_key = os.getenv("AIzaSyDZPNiZEXhiVtGBjC7gUt7g15x4Wow7kCI")
print(f"Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: No API Key found.")
    exit(1)

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key
)

try:
    print("Attempting to invoke model...")
    response = llm.invoke("Hello, are you working?")
    print("Success!")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")
