"""
Enhanced main.py with detailed debugging output and cross-platform timeout
This version works on both Windows and Unix systems
"""
import os
import sys
import traceback
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main function with enhanced error handling and debugging"""
    print("🚀 Starting Stock Analysis AI...")
    print("=" * 60)
    
    try:
        # Step 1: Test basic imports
        print("📦 Step 1: Testing imports...")
        
        try:
            from config import config
            print("✅ Config imported successfully")
        except Exception as e:
            print(f"❌ Config import failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        try:
            from agents import create_financial_team
            print("✅ Agents module imported successfully")
        except Exception as e:
            print(f"❌ Agents import failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        try:
            from tasks import create_quick_analysis_workflow
            print("✅ Tasks module imported successfully")
        except Exception as e:
            print(f"❌ Tasks import failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        # Step 2: Test LLM connection
        print("\n🔑 Step 2: Testing LLM connection...")
        
        try:
            llm = config.get_llm()
            print("✅ LLM configuration loaded")
            
            # Test a simple call with timeout
            test_response = run_with_timeout(
                lambda: llm.invoke("Respond with: LLM connection test successful"),
                timeout=30,  # 30 second timeout for LLM test
                description="LLM connection test"
            )
            
            if test_response is not None:
                print(f"✅ LLM connection test successful: {test_response.content}")
            else:
                print("❌ LLM connection test timed out")
                return
                
        except Exception as e:
            print(f"❌ LLM connection failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        # Step 3: Create agents
        print("\n👥 Step 3: Creating agents...")
        
        try:
            agents = create_financial_team()
            print(f"✅ Created {len(agents)} agents: {list(agents.keys())}")
        except Exception as e:
            print(f"❌ Agent creation failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        # Step 4: Get user input
        print("\n📝 Step 4: Getting user input...")
        
        # Simple test input instead of complex user interaction
        stock_symbol = "AAPL"  # Test with a simple stock
        investor_profile = {
            "goals": "Long-term growth",
            "risk_tolerance": "moderate",
            "investment_horizon": "5+ years",
            "investment_amount": "$10,000"
        }
        
        print(f"✅ Using test data: {stock_symbol}, profile: {investor_profile}")
        
        # Step 5: Create tasks
        print("\n📋 Step 5: Creating tasks...")
        
        try:
            tasks = create_quick_analysis_workflow(agents, stock_symbol, investor_profile)
            print(f"✅ Created {len(tasks)} tasks")
        except Exception as e:
            print(f"❌ Task creation failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return
            
        # Step 6: Create and run crew
        print("\n🤖 Step 6: Creating and running crew...")
        
        try:
            from crewai import Crew
            
            # Create crew with minimal configuration for testing
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True,  # Enable verbose for debugging
                max_rpm=10,    # Limit requests per minute
                memory=False   # Disable memory to avoid potential issues
            )
            
            print("✅ Crew created successfully")
            print("🚀 Starting crew execution...")
            
            # Run the crew with cross-platform timeout handling
            result = run_with_timeout(
                crew.kickoff,
                timeout=300,  # 5 minutes
                description="Crew execution"
            )
            
            if result is not None:
                print("\n" + "=" * 60)
                print("📊 ANALYSIS RESULTS")
                print("=" * 60)
                print(f"✅ Analysis completed successfully!")
                print(f"📄 Result: {result}")
            else:
                print("❌ Analysis timed out after 5 minutes")
                return
                
        except Exception as e:
            print(f"❌ Crew execution failed: {e}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            
            # Additional debugging for connection errors
            error_str = str(e).lower()
            if "connection" in error_str:
                print("\n🔍 CONNECTION ERROR DEBUGGING:")
                print("- Check your internet connection")
                print("- Verify Google API key is valid")
                print("- Ensure Generative AI API is enabled in Google Cloud")
                print("- Check if there are any firewall/proxy issues")
                
            return
            
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted by user")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"📍 Full traceback: {traceback.format_exc()}")
        return

def run_with_timeout(func, timeout, description="Operation"):
    """
    Cross-platform timeout implementation using threading
    Works on both Windows and Unix systems
    """
    result = [None]  # Use list to allow modification in nested function
    exception = [None]
    
    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e
    
    print(f"⏱️ Running {description} with {timeout}s timeout...")
    
    thread = threading.Thread(target=target)
    thread.daemon = True  # Dies when main thread dies
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"⏰ {description} timed out after {timeout} seconds")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

def check_environment():
    """Check environment setup before running main"""
    print("🔧 Checking environment setup...")
    
    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("💡 Make sure your .env file contains:")
        for var in missing_vars:
            print(f"   {var}=your_key_here")
        return False
    
    print("✅ Environment variables check passed")
    return True

if __name__ == "__main__":
    print("🔧 Stock Analysis AI - Enhanced Debug Version (Cross-Platform)")
    print("=" * 60)
    
    # Check environment first
    if not check_environment():
        sys.exit(1)
    
    # Run main function
    main()
    
    print("\n" + "=" * 60)
    print("🏁 Process completed")