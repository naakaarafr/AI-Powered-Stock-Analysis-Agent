"""
Configuration module for the Stock Analysis CrewAI project.
Handles environment setup and API key validation.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for managing API keys and settings."""
    
    def __init__(self):
        self._setup_environment()
        self._validate_keys()
    
    def _setup_environment(self):
        """Setup environment variables to force Gemini usage."""
        # Force CrewAI to avoid OpenAI
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["OPENAI_MODEL_NAME"] = ""
        os.environ["OPENAI_API_BASE"] = ""
        
        # Set API keys from environment
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.sec_api_key = os.getenv("SEC_API_API_KEY")
    
    def _validate_keys(self):
        """Validate required API keys."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")
        
        if not self.serper_api_key:
            print("Warning: SERPER_API_KEY not found. Search functionality will be limited.")
        
        if not self.sec_api_key:
            print("Warning: SEC_API_API_KEY not found. SEC filing tools will not work.")
    
    def get_llm(self):
        """Get configured Gemini LLM instance."""
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.google_api_key,
                temperature=0.5,
                verbose=False
            )
            # Test connection
            llm.invoke("test")
            return llm
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Gemini LLM: {e}")
    
    def display_status(self):
        """Display configuration status."""
        print("🔧 Stock Analysis AI Configuration")
        print(f"📍 Google API Key: {'✅ Found' if self.google_api_key else '❌ Missing'}")
        print(f"🔍 Serper API Key: {'✅ Found' if self.serper_api_key else '❌ Missing'}")
        print(f"📋 SEC API Key: {'✅ Found' if self.sec_api_key else '❌ Missing'}")
        print("✅ Configuration loaded - CrewAI will use Gemini exclusively")

# Global config instance
config = Config()