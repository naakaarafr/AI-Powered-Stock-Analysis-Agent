"""
Debug script to test API connections and identify issues
Run this first before running your main crew.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_internet_connection():
    """Test basic internet connectivity"""
    print("🌐 Testing internet connection...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection: OK")
            return True
        else:
            print(f"❌ Internet connection issue: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Internet connection failed: {e}")
        return False

def test_google_api_key():
    """Test Google API key validity"""
    print("\n🔑 Testing Google API key...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    if len(api_key) < 30:
        print(f"❌ API key seems too short: {len(api_key)} characters")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]} ({len(api_key)} chars)")
    
    # Test the API key with a simple request
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        print("📡 Testing connection to Google Generative AI API...")
        
        # Use the same model as in your config.py
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.5,
            verbose=False
        )
        
        # Simple test message
        print("🔄 Sending test message to Gemini...")
        response = llm.invoke("Hello, respond with just 'API Working'")
        print(f"✅ Google API test successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Google API test failed: {e}")
        # Check for common error types
        error_str = str(e).lower()
        if "connection" in error_str:
            print("💡 Network connection issue. Check your internet connection.")
        elif "permission denied" in error_str or "403" in error_str:
            print("💡 This might be an API permissions issue. Check if Generative AI API is enabled.")
        elif "quota" in error_str or "429" in error_str:
            print("💡 This might be a quota/billing issue. Check your Google Cloud billing.")
        elif "invalid api key" in error_str or "401" in error_str:
            print("💡 The API key appears to be invalid. Please regenerate it.")
        elif "timeout" in error_str:
            print("💡 Request timed out. Try again or check your network.")
        elif "ssl" in error_str:
            print("💡 SSL certificate issue. Check your system time and certificates.")
        return False

def test_serper_api_key():
    """Test Serper API key validity"""
    print("\n🔍 Testing Serper API key...")
    
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("❌ SERPER_API_KEY not found in environment (optional but recommended)")
        return False
    
    print(f"✅ Serper API key found: {api_key[:8]}...{api_key[-4:]} ({len(api_key)} chars)")
    
    # Test Serper API
    try:
        url = "https://google.serper.dev/search"
        payload = {"q": "test query", "num": 3}
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Serper API test successful - Found {len(result.get('organic', []))} results")
            return True
        elif response.status_code == 401:
            print("❌ Serper API test failed: Invalid API key")
            return False
        elif response.status_code == 429:
            print("❌ Serper API test failed: Rate limit exceeded")
            return False
        else:
            print(f"❌ Serper API test failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Serper API test failed: {e}")
        return False

def test_sec_api_key():
    """Test SEC API key validity"""
    print("\n📋 Testing SEC API key...")
    
    api_key = os.getenv("SEC_API_API_KEY")
    if not api_key:
        print("❌ SEC_API_API_KEY not found in environment (optional)")
        return False
    
    print(f"✅ SEC API key found: {api_key[:8]}...{api_key[-4:]} ({len(api_key)} chars)")
    
    # Test SEC API with a simple query
    try:
        # Try importing sec_api
        try:
            from sec_api import QueryApi
        except ImportError:
            print("⚠️ sec-api package not installed. SEC tools will not work.")
            print("💡 Install with: pip install sec-api")
            return False
        
        query_api = QueryApi(api_key=api_key)
        
        # Simple test query
        query = {
            "query": {
                "query_string": {
                    "query": "ticker:AAPL AND formType:\"10-K\""
                }
            },
            "from": "0",
            "size": "1"
        }
        
        response = query_api.get_filings(query)
        
        if response and 'filings' in response:
            print(f"✅ SEC API test successful - Found {len(response['filings'])} filings")
            return True
        else:
            print("❌ SEC API test failed: No valid response")
            return False
            
    except Exception as e:
        print(f"❌ SEC API test failed: {e}")
        error_str = str(e).lower()
        if "unauthorized" in error_str or "401" in error_str:
            print("💡 This might be an invalid SEC API key.")
        elif "forbidden" in error_str or "403" in error_str:
            print("💡 This might be an API permissions issue.")
        return False

def test_crewai_gemini():
    """Test CrewAI with Gemini integration"""
    print("\n🤖 Testing CrewAI with Gemini...")
    
    try:
        # Import your config to test it
        print("📦 Importing config...")
        from config import config
        
        # Test getting LLM from config
        print("🔧 Getting LLM from config...")
        llm = config.get_llm()
        
        # Test direct LLM call first
        print("🔄 Testing direct LLM call...")
        test_response = llm.invoke("Say 'CrewAI test successful'")
        print(f"✅ Direct LLM call successful: {test_response.content}")
        
        # Create a simple test agent
        print("👤 Creating test agent...")
        from crewai import Agent
        
        test_agent = Agent(
            role="Test Agent",
            goal="Test if CrewAI works with Gemini",
            backstory="I am a test agent to verify the setup",
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        # Test agent execution
        print("🎯 Testing agent execution...")
        from crewai import Task, Crew
        
        test_task = Task(
            description="Say 'Agent test successful'",
            expected_output="The exact phrase 'Agent test successful'",
            agent=test_agent
        )
        
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            verbose=False
        )
        
        print("🚀 Running test crew...")
        result = test_crew.kickoff()
        print(f"✅ CrewAI test successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewAI with Gemini test failed: {e}")
        error_str = str(e).lower()
        if "openai" in error_str:
            print("💡 This might be an OpenAI conflict. Make sure OPENAI_API_KEY is empty.")
        elif "connection" in error_str:
            print("💡 Connection issue. Check your internet and API key.")
        elif "timeout" in error_str:
            print("💡 Request timed out. Check your network connection.")
        elif "config" in error_str:
            print("💡 Configuration issue. Check your config.py file.")
        return False

def test_tools():
    """Test custom tools"""
    print("\n🔧 Testing custom tools...")
    
    try:
        from tools import available_tools, financial_calculator, analyze_stock_metrics
        
        # Test financial calculator using _run method
        try:
            calc_result = financial_calculator._run("100 * 0.15")
            if "15.0" in calc_result:
                print("✅ Financial calculator working")
            else:
                print(f"❌ Financial calculator unexpected result: {calc_result}")
                return False
        except Exception as e:
            print(f"❌ Financial calculator error: {e}")
            return False
        
        # Test stock metrics analyzer using _run method
        try:
            metrics_result = analyze_stock_metrics._run("price=100,volume=1000000,market_cap=5000000000")
            if "Current Price" in metrics_result:
                print("✅ Stock metrics analyzer working")
            else:
                print(f"❌ Stock metrics analyzer unexpected result: {metrics_result}")
                return False
        except Exception as e:
            print(f"❌ Stock metrics analyzer error: {e}")
            return False
        
        # Test that all tools are properly configured
        working_tools = 0
        for tool in available_tools:
            try:
                tool_name = getattr(tool, 'name', type(tool).__name__)
                if hasattr(tool, '_run'):
                    print(f"✅ Tool '{tool_name}' properly configured")
                    working_tools += 1
                else:
                    print(f"❌ Tool '{tool_name}' missing _run method")
            except Exception as e:
                print(f"❌ Error checking tool: {e}")
        
        print(f"✅ Available tools: {working_tools}/{len(available_tools)} tools working")
        return working_tools > 0
        
    except ImportError as e:
        print(f"❌ Tools import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def test_agents_and_tasks():
    """Test agents and tasks creation"""
    print("\n👥 Testing agents and tasks...")
    
    try:
        from agents import create_financial_team
        from tasks import create_quick_analysis_workflow
        
        # Create agents
        agents = create_financial_team()
        
        required_agents = ["research_analyst", "financial_analyst", "investment_advisor", "market_strategist"]
        for agent_name in required_agents:
            if agent_name not in agents:
                print(f"❌ Missing agent: {agent_name}")
                return False
        
        # Test task creation
        investor_profile = {
            "goals": "test",
            "risk_tolerance": "moderate",
            "investment_horizon": "long-term",
            "investment_amount": "$10,000"
        }
        
        tasks = create_quick_analysis_workflow(agents, "AAPL", investor_profile)
        
        if len(tasks) > 0:
            print(f"✅ Agents and tasks working - Created {len(agents)} agents and {len(tasks)} tasks")
            return True
        else:
            print("❌ No tasks created")
            return False
        
    except Exception as e:
        print(f"❌ Agents and tasks test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 Stock Analysis AI - API Connection Diagnostic Tool")
    print("=" * 60)
    
    tests = [
        ("Internet Connection", test_internet_connection),
        ("Google API Key", test_google_api_key),
        ("Serper API Key", test_serper_api_key),
        ("SEC API Key", test_sec_api_key),
        ("CrewAI + Gemini", test_crewai_gemini),
        ("Custom Tools", test_tools),
        ("Agents and Tasks", test_agents_and_tasks)
    ]
    
    results = {}
    critical_tests = ["Internet Connection", "Google API Key", "CrewAI + Gemini", "Custom Tools", "Agents and Tasks"]
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    critical_passed = 0
    optional_passed = 0
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        is_critical = test_name in critical_tests
        category = "CRITICAL" if is_critical else "OPTIONAL"
        
        print(f"{test_name}: {status} ({category})")
        
        if is_critical and passed:
            critical_passed += 1
        elif not is_critical and passed:
            optional_passed += 1
    
    total_critical = len(critical_tests)
    
    print(f"\nCritical Tests: {critical_passed}/{total_critical} passed")
    print(f"Optional Tests: {optional_passed}/{len(tests) - total_critical} passed")
    
    if critical_passed == total_critical:
        print("\n🎉 All critical tests passed! Your setup should work.")
        if optional_passed < (len(tests) - total_critical):
            print("⚠️  Some optional features may not work (Serper search, SEC filings).")
    else:
        print("\n⚠️  Critical tests failed. Please fix the issues above before running your main script.")
        
        # Provide specific guidance
        if not results.get("Internet Connection"):
            print("\n💡 Fix: Check your internet connection")
        
        if not results.get("Google API Key"):
            print("\n💡 Fix: Check your Google API key:")
            print("   1. Go to https://console.cloud.google.com/")
            print("   2. Enable the Generative AI API")
            print("   3. Create an API key")
            print("   4. Add it to your .env file as GOOGLE_API_KEY=your_key_here")
        
        if not results.get("Serper API Key"):
            print("\n💡 Fix: Get Serper API key (optional but recommended):")
            print("   1. Go to https://serper.dev/")
            print("   2. Sign up and get an API key")
            print("   3. Add it to your .env file as SERPER_API_KEY=your_key_here")
        
        if not results.get("SEC API Key"):
            print("\n💡 Fix: Get SEC API key (optional):")
            print("   1. Go to https://sec-api.io/")
            print("   2. Sign up and get an API key")
            print("   3. Add it to your .env file as SEC_API_API_KEY=your_key_here")
            print("   4. Install sec-api: pip install sec-api")

if __name__ == "__main__":
    main()