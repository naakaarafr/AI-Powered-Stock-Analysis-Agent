#!/usr/bin/env python3
"""
Enhanced main.py with step-by-step execution and better error handling.
Uses the same successful patterns as main_test.py but with full CLI functionality.
Now includes robust comprehensive analysis support.
"""
import argparse
import sys
import os
import asyncio
import threading
import time
import traceback
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import concurrent.futures

# Load environment variables
load_dotenv()

def run_with_timeout(func, timeout, description="Operation"):
    """
    Cross-platform timeout implementation using threading.
    Works on both Windows and Unix systems.
    """
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e
    
    print(f"⏱️ Running {description} with {timeout}s timeout...")
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"⏰ {description} timed out after {timeout} seconds")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

def check_environment():
    """Check environment setup before running main."""
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

def test_imports():
    """Test all required imports step by step."""
    print("📦 Testing imports...")
    
    imports = {}
    
    try:
        from config import config
        imports['config'] = config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return None
        
    try:
        from agents import create_financial_team
        imports['create_financial_team'] = create_financial_team
        print("✅ Agents module imported successfully")
    except Exception as e:
        print(f"❌ Agents import failed: {e}")
        return None
        
    try:
        from tasks import create_quick_analysis_workflow
        imports['create_quick_analysis_workflow'] = create_quick_analysis_workflow
        print("✅ Quick analysis workflow imported successfully")
        
        # Try to import comprehensive workflow
        try:
            from tasks import create_comprehensive_analysis_workflow
            imports['create_comprehensive_analysis_workflow'] = create_comprehensive_analysis_workflow
            print("✅ Comprehensive analysis workflow imported successfully")
        except ImportError as ie:
            print(f"⚠️ Comprehensive analysis workflow not available: {ie}")
            print("ℹ️ Only quick analysis will be available")
        except Exception as e:
            print(f"⚠️ Error importing comprehensive workflow: {e}")
            print("ℹ️ Falling back to quick analysis only")
            
    except Exception as e:
        print(f"❌ Tasks import failed: {e}")
        return None
    
    try:
        from crewai import Crew
        imports['Crew'] = Crew
        print("✅ CrewAI imported successfully")
    except Exception as e:
        print(f"❌ CrewAI import failed: {e}")
        return None
    
    return imports

def test_llm_connection(config):
    """Test LLM connection step by step."""
    print("🔑 Testing LLM connection...")
    
    try:
        llm = config.get_llm()
        print("✅ LLM configuration loaded")
        
        # Test with timeout
        test_response = run_with_timeout(
            lambda: llm.invoke("Respond with: Connection test successful"),
            timeout=30,
            description="LLM connection test"
        )
        
        if test_response is not None:
            print(f"✅ LLM connection test successful")
            return llm
        else:
            print("❌ LLM connection test timed out")
            return None
            
    except Exception as e:
        print(f"❌ LLM connection failed: {e}")
        error_str = str(e).lower()
        if "connection" in error_str:
            print("\n🔍 CONNECTION ERROR TROUBLESHOOTING:")
            print("- Check your internet connection")
            print("- Verify Google API key is valid")
            print("- Ensure Generative AI API is enabled in Google Cloud")
            print("- Check if there are firewall/proxy issues")
        return None

def create_agents_safely(create_financial_team):
    """Create agents with error handling."""
    print("👥 Creating agents...")
    
    try:
        agents = create_financial_team()
        print(f"✅ Created {len(agents)} agents: {list(agents.keys())}")
        return agents
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        return None

def create_tasks_safely(create_task_func, agents, stocks, investor_profile, comprehensive=False):
    """Create tasks with error handling and proper comprehensive analysis support."""
    print("📋 Creating tasks...")
    
    try:
        if comprehensive:
            # For comprehensive analysis, handle multiple stocks properly
            print(f"🔍 Setting up comprehensive analysis for {len(stocks)} stocks...")
            all_tasks = []
            
            # Check if the comprehensive function expects individual stocks or a list
            try:
                # Try with the first stock to test the function signature
                test_tasks = create_task_func(agents, stocks[0], investor_profile)
                
                # If successful, create tasks for each stock individually
                for i, stock in enumerate(stocks):
                    print(f"   📊 Creating tasks for {stock} ({i+1}/{len(stocks)})...")
                    stock_tasks = create_task_func(agents, stock, investor_profile)
                    
                    # Add stock identifier to task descriptions if multiple stocks
                    if len(stocks) > 1:
                        for task in stock_tasks:
                            if hasattr(task, 'description'):
                                task.description = f"[{stock}] {task.description}"
                            elif hasattr(task, 'task_description'):
                                task.task_description = f"[{stock}] {task.task_description}"
                    
                    all_tasks.extend(stock_tasks)
                    
            except Exception as e:
                # If individual stock approach fails, try passing the entire list
                print(f"   ℹ️ Trying alternative approach for comprehensive analysis...")
                all_tasks = create_task_func(agents, stocks, investor_profile)
            
            print(f"✅ Created {len(all_tasks)} comprehensive tasks for {len(stocks)} stock(s)")
            return all_tasks
        else:
            # For quick analysis, use the primary stock or the list as appropriate
            try:
                # Try with the list first
                tasks = create_task_func(agents, stocks, investor_profile)
                print(f"✅ Created {len(tasks)} quick analysis tasks for multiple stocks")
                return tasks
            except Exception:
                # Fall back to using just the first stock
                primary_stock = stocks[0] if stocks else "AAPL"
                tasks = create_task_func(agents, primary_stock, investor_profile)
                print(f"✅ Created {len(tasks)} quick analysis tasks for {primary_stock}")
                return tasks
                
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        
        # Provide specific guidance for comprehensive analysis issues
        if comprehensive:
            print("\n🔍 COMPREHENSIVE ANALYSIS TROUBLESHOOTING:")
            print("- Ensure tasks.py has create_comprehensive_analysis_workflow function")
            print("- Check that the function accepts (agents, stocks, investor_profile) parameters")
            print("- Verify that all required dependencies are installed")
            print("- Try using quick analysis (-q) as an alternative")
        
        return None

def run_crew_analysis(Crew, agents, tasks, timeout=300, no_timeout=False, comprehensive=False):
    """Run crew analysis with proper error handling and comprehensive analysis support."""
    print("🤖 Creating and running crew...")
    
    try:
        # Adjust crew settings based on analysis type
        if comprehensive:
            # More conservative settings for comprehensive analysis
            max_rpm = 5  # Lower rate limit for comprehensive analysis
            verbose_level = 2  # More detailed logging
            timeout_multiplier = 2  # Give more time for comprehensive analysis
        else:
            # Standard settings for quick analysis
            max_rpm = 10
            verbose_level = 1
            timeout_multiplier = 1
        
        # Create crew with appropriate settings
        crew_config = {
            "agents": list(agents.values()),
            "tasks": tasks,
            "verbose": verbose_level,
            "max_rpm": max_rpm,
            "memory": False  # Disable memory to avoid issues
        }
        
        # Add additional settings for comprehensive analysis
        if comprehensive:
            crew_config.update({
                "max_execution_time": timeout * timeout_multiplier if not no_timeout else None,
                "step_callback": lambda step: print(f"🔄 Step completed: {step.get('description', 'Unknown step')}")
            })
        
        crew = Crew(**crew_config)
        
        print("✅ Crew created successfully")
        
        analysis_type = "comprehensive" if comprehensive else "quick"
        print(f"🚀 Starting {analysis_type} analysis...")
        
        if comprehensive:
            print("ℹ️ Comprehensive analysis may take significantly longer...")
            print("ℹ️ Please be patient as we perform detailed analysis...")
        
        if no_timeout:
            print("⏱️ Running without timeout...")
            result = crew.kickoff()
        else:
            effective_timeout = timeout * timeout_multiplier if comprehensive else timeout
            result = run_with_timeout(
                crew.kickoff,
                timeout=effective_timeout,
                description=f"{analysis_type.capitalize()} crew execution"
            )
        
        return result
        
    except Exception as e:
        print(f"❌ Crew execution failed: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        
        # Provide specific guidance based on error type
        error_str = str(e).lower()
        if "timeout" in error_str or "time" in error_str:
            print("\n🔍 TIMEOUT ERROR SOLUTIONS:")
            print("- Try using --no-timeout flag")
            print("- Increase timeout with --timeout <seconds>")
            print("- Use quick analysis (-q) for faster results")
        elif "memory" in error_str or "resource" in error_str:
            print("\n🔍 RESOURCE ERROR SOLUTIONS:")
            print("- Reduce number of stocks being analyzed")
            print("- Use quick analysis (-q) instead of comprehensive")
            print("- Restart the application to clear memory")
        
        return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Stock Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -s AAPL MSFT GOOGL -g "long-term growth" -r moderate
  python main.py -s TSLA NVDA -q --goals "aggressive growth" --risk high
  python main.py -s SPY QQQ --comprehensive --timeout 600
  python main.py -s AAPL -c --no-timeout --verbose
        """
    )
    
    # Required arguments
    parser.add_argument(
        "-s", "--stocks",
        nargs="+",
        required=True,
        help="Stock ticker symbols to analyze (e.g., AAPL MSFT GOOGL)"
    )
    
    # Analysis type
    analysis_group = parser.add_mutually_exclusive_group()
    analysis_group.add_argument(
        "-q", "--quick",
        action="store_true",
        help="Run quick analysis (faster, more reliable)"
    )
    analysis_group.add_argument(
        "-c", "--comprehensive",
        action="store_true",
        help="Run comprehensive analysis (slower, more detailed)"
    )
    
    # Investor profile
    parser.add_argument(
        "-g", "--goals",
        default="long-term growth",
        help="Investment goals (default: long-term growth)"
    )
    parser.add_argument(
        "-r", "--risk",
        choices=["conservative", "moderate", "aggressive", "high"],
        default="moderate",
        help="Risk tolerance (default: moderate)"
    )
    parser.add_argument(
        "-t", "--horizon",
        choices=["short-term", "medium-term", "long-term", "5+ years"],
        default="long-term",
        help="Investment time horizon (default: long-term)"
    )
    parser.add_argument(
        "-a", "--amount",
        default="$10,000",
        help="Investment amount (default: $10,000)"
    )
    
    # Timeout options
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Analysis timeout in seconds (default: 300, comprehensive gets 2x)"
    )
    
    # Execution mode
    parser.add_argument(
        "--no-timeout",
        action="store_true",
        help="Disable timeout (run analysis without time limits)"
    )
    
    # Output options
    parser.add_argument(
        "-o", "--output",
        help="Save results to file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def validate_stocks(stocks: List[str]) -> List[str]:
    """Validate and clean stock ticker symbols."""
    valid_stocks = []
    for stock in stocks:
        ticker = stock.upper().strip()
        if len(ticker) >= 1 and len(ticker) <= 5 and ticker.isalnum():
            valid_stocks.append(ticker)
        else:
            print(f"⚠️ Warning: Skipping invalid ticker symbol: {stock}")
    return valid_stocks

def save_results(results: str, filename: str):
    """Save analysis results to file, creating directories if needed."""
    try:
        # Normalize the path to handle different OS path separators
        filename = os.path.normpath(filename)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {os.path.abspath(directory)}")
        
        # Write the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(results))
        
        # Show the absolute path where file was saved
        abs_path = os.path.abspath(filename)
        print(f"💾 Results saved to: {abs_path}")
        
        # Verify the file was actually created
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"✅ File confirmed: {file_size} bytes written")
        else:
            print(f"⚠️ Warning: File may not have been created properly")
            
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
        print(f"📍 Attempted path: {os.path.abspath(filename) if filename else 'None'}")
        print(f"📍 Current working directory: {os.getcwd()}")

def main():
    """Main application entry point with step-by-step execution."""
    print("🎯 AI-Powered Stock Analysis Tool (Enhanced v4 - Comprehensive Support)")
    print("=" * 70)
    
    # Step 1: Check environment
    if not check_environment():
        sys.exit(1)
    
    # Step 2: Parse arguments
    args = parse_arguments()
    
    # Step 3: Validate stocks
    stocks = validate_stocks(args.stocks)
    if not stocks:
        print("❌ Error: No valid stock ticker symbols provided")
        sys.exit(1)
    
    print(f"📈 Analyzing stocks: {', '.join(stocks)}")
    
    # Step 4: Test imports
    imports = test_imports()
    if not imports:
        print("❌ Import test failed. Cannot proceed.")
        sys.exit(1)
    
    # Step 5: Test LLM connection
    llm = test_llm_connection(imports['config'])
    if not llm:
        print("❌ LLM connection test failed. Cannot proceed.")
        sys.exit(1)
    
    # Step 6: Create investor profile
    investor_profile = {
        "goals": args.goals,
        "risk_tolerance": args.risk,
        "investment_horizon": args.horizon,
        "investment_amount": args.amount
    }
    
    if args.verbose:
        print(f"👤 Investor Profile: {investor_profile}")
    
    try:
        # Step 7: Create agents
        agents = create_agents_safely(imports['create_financial_team'])
        if not agents:
            print("❌ Agent creation failed. Cannot proceed.")
            sys.exit(1)
        
        # Step 8: Determine analysis type
        comprehensive = args.comprehensive
        quick = args.quick
        
        # Check if comprehensive analysis is available
        has_comprehensive = 'create_comprehensive_analysis_workflow' in imports
        
        if comprehensive and not has_comprehensive:
            print("❌ Comprehensive analysis requested but not available!")
            print("💡 Please ensure your tasks.py includes create_comprehensive_analysis_workflow")
            print("💡 Falling back to quick analysis...")
            quick = True
            comprehensive = False
        
        # Default to quick analysis if neither specified
        if not comprehensive and not quick:
            quick = True
            print("📝 Defaulting to quick analysis")
        
        # Step 9: Create tasks
        if quick:
            print("⚡ Setting up quick analysis...")
            tasks = create_tasks_safely(
                imports['create_quick_analysis_workflow'],
                agents,
                stocks,
                investor_profile,
                comprehensive=False
            )
            analysis_type = "quick"
        else:
            print("🔍 Setting up comprehensive analysis...")
            tasks = create_tasks_safely(
                imports['create_comprehensive_analysis_workflow'],
                agents,
                stocks,
                investor_profile,
                comprehensive=True
            )
            analysis_type = "comprehensive"
        
        if not tasks:
            print("❌ Task creation failed. Cannot proceed.")
            sys.exit(1)
        
        # Step 10: Run analysis
        print(f"\n🚀 Starting {analysis_type} analysis...")
        if not args.no_timeout:
            effective_timeout = args.timeout * 2 if comprehensive else args.timeout
            print(f"⏱️ Timeout set to {effective_timeout} seconds")
        
        result = run_crew_analysis(
            imports['Crew'],
            agents,
            tasks,
            timeout=args.timeout,
            no_timeout=args.no_timeout,
            comprehensive=comprehensive
        )
        
        # Step 11: Handle results
        if result is not None:
            print("\n" + "=" * 80)
            print(f"📊 {analysis_type.upper()} ANALYSIS RESULTS")
            print("=" * 80)
            print(result)
            print("=" * 80)
            
            # Save results if requested
            if args.output:
                save_results(result, args.output)
            else:
                # Auto-save with timestamp and analysis type
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                analysis_dir = os.path.join(os.getcwd(), "analysis")
                
                # Ensure the analysis directory exists
                if not os.path.exists(analysis_dir):
                    try:
                        os.makedirs(analysis_dir, exist_ok=True)
                        print(f"📁 Created analysis directory: {os.path.abspath(analysis_dir)}")
                    except Exception as e:
                        print(f"❌ Failed to create analysis directory: {e}")
                        analysis_dir = os.getcwd()  # Fall back to current directory
                        print(f"📁 Falling back to current directory: {analysis_dir}")
                
                # Create the full file path
                auto_filename = os.path.join(analysis_dir, f"{analysis_type}_analysis_{timestamp}.txt")
                print(f"💾 Auto-saving to: {os.path.abspath(auto_filename)}")
                save_results(result, auto_filename)
            
            print(f"✅ {analysis_type.capitalize()} analysis completed successfully!")
        else:
            print(f"❌ {analysis_type.capitalize()} analysis failed or timed out")
            if comprehensive:
                print("💡 Try using quick analysis mode (-q) or increasing timeout (--timeout 600)")
            else:
                print("💡 Try increasing timeout or using --no-timeout")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            print(f"📍 Full traceback: {traceback.format_exc()}")
        
        # Provide specific error guidance
        error_str = str(e).lower()
        if "connection" in error_str:
            print("\n🔍 CONNECTION ERROR SOLUTIONS:")
            print("- Check internet connection")
            print("- Verify API key is valid")
            print("- Try running with --no-timeout")
        elif "comprehensive" in error_str:
            print("\n🔍 COMPREHENSIVE ANALYSIS ERROR SOLUTIONS:")
            print("- Ensure tasks.py has create_comprehensive_analysis_workflow function")
            print("- Try quick analysis with -q flag")
            print("- Check that all dependencies are properly installed")
        
        sys.exit(1)

def interactive_mode():
    """Run in interactive mode with step-by-step execution."""
    print("🎯 Interactive Stock Analysis Mode (Enhanced v4 - Comprehensive Support)")
    print("=" * 70)
    
    # Check environment first
    if not check_environment():
        return
    
    # Test imports
    imports = test_imports()
    if not imports:
        print("❌ Import test failed. Cannot proceed.")
        return
    
    # Test LLM connection
    llm = test_llm_connection(imports['config'])
    if not llm:
        print("❌ LLM connection test failed. Cannot proceed.")
        return
    
    try:
        # Get user input
        while True:
            stocks_input = input("📈 Enter stock symbols (comma-separated): ").strip()
            if stocks_input:
                stocks = [s.strip().upper() for s in stocks_input.split(",")]
                stocks = validate_stocks(stocks)
                if stocks:
                    break
            print("Please enter valid stock ticker symbols (e.g., AAPL, MSFT, GOOGL)")
        
        print(f"Selected stocks: {', '.join(stocks)}")
        
        # Get investor profile
        print("\n👤 Investor Profile Setup:")
        goals = input("Investment goals [long-term growth]: ").strip() or "long-term growth"
        
        risk_options = ["conservative", "moderate", "aggressive"]
        while True:
            risk = input(f"Risk tolerance {risk_options} [moderate]: ").strip().lower() or "moderate"
            if risk in risk_options:
                break
            print(f"Please choose from: {', '.join(risk_options)}")
        
        horizon_options = ["short-term", "medium-term", "long-term", "5+ years"]
        while True:
            horizon = input(f"Investment horizon {horizon_options} [long-term]: ").strip() or "long-term"
            if horizon in horizon_options:
                break
            print(f"Please choose from: {', '.join(horizon_options)}")
        
        amount = input("Investment amount [$10,000]: ").strip() or "$10,000"
        
        # Analysis type
        print("\n📊 Analysis Options:")
        has_comprehensive = 'create_comprehensive_analysis_workflow' in imports
        
        if has_comprehensive:
            print("1. Quick Analysis (faster, more reliable)")
            print("2. Comprehensive Analysis (detailed, may take longer)")
            max_choice = "2"
        else:
            print("1. Quick Analysis (only option available)")
            print("ℹ️ Comprehensive analysis not available - missing create_comprehensive_analysis_workflow")
            max_choice = "1"
        
        while True:
            choice = input("Choose analysis type [1]: ").strip() or "1"
            if choice in ["1"] or (choice == "2" and max_choice == "2"):
                break
            if max_choice == "1":
                print("Only quick analysis is available")
                choice = "1"
                break
            else:
                print("Please enter 1 or 2")
        
        quick_analysis = choice == "1"
        comprehensive_analysis = choice == "2"
        
        # Timeout selection for comprehensive analysis
        timeout = 300  # Default
        if comprehensive_analysis:
            print("\n⏱️ Comprehensive analysis typically takes longer:")
            print("1. Standard timeout (5 minutes)")
            print("2. Extended timeout (10 minutes)") 
            print("3. No timeout (unlimited)")
            
            timeout_choice = input("Choose timeout option [1]: ").strip() or "1"
            if timeout_choice == "2":
                timeout = 600
            elif timeout_choice == "3":
                timeout = None
                print("⚠️ Running without timeout - analysis may take a very long time")
            
        # Create investor profile
        investor_profile = {
            "goals": goals,
            "risk_tolerance": risk,
            "investment_horizon": horizon,
            "investment_amount": amount
        }
        
        # Create agents
        agents = create_agents_safely(imports['create_financial_team'])
        if not agents:
            print("❌ Agent creation failed.")
            return
        
        # Create tasks
        if quick_analysis:
            print("⚡ Setting up quick analysis...")
            tasks = create_tasks_safely(
                imports['create_quick_analysis_workflow'],
                agents,
                stocks,
                investor_profile,
                comprehensive=False
            )
            analysis_type = "quick"
        else:
            print("🔍 Setting up comprehensive analysis...")
            tasks = create_tasks_safely(
                imports['create_comprehensive_analysis_workflow'],
                agents,
                stocks,
                investor_profile,
                comprehensive=True
            )
            analysis_type = "comprehensive"
        
        if not tasks:
            print("❌ Task creation failed.")
            return
        
        # Run analysis
        print(f"\n🚀 Starting {analysis_type} analysis...")
        if comprehensive_analysis:
            print("ℹ️ Comprehensive analysis includes detailed technical, fundamental, and sentiment analysis")
            print("ℹ️ Please be patient - this may take several minutes...")
        
        result = run_crew_analysis(
            imports['Crew'],
            agents,
            tasks,
            timeout=timeout or 300,
            no_timeout=(timeout is None),
            comprehensive=comprehensive_analysis
        )
        
        # Display results
        if result is not None:
            print("\n" + "=" * 80)
            print(f"📊 {analysis_type.upper()} ANALYSIS RESULTS")
            print("=" * 80)
            print(result)
            print("=" * 80)
            
            # Ask to save
            save_choice = input("\n💾 Save results to file? (y/N): ").strip().lower()
            if save_choice in ['y', 'yes']:
                # Create analysis folder if it doesn't exist
                analysis_dir = os.path.join(os.getcwd(), "analysis")
                
                try:
                    if not os.path.exists(analysis_dir):
                        os.makedirs(analysis_dir, exist_ok=True)
                        print(f"📁 Created analysis directory: {os.path.abspath(analysis_dir)}")
                except Exception as e:
                    print(f"❌ Failed to create analysis directory: {e}")
                    analysis_dir = os.getcwd()  # Fall back to current directory
                    print(f"📁 Using current directory instead: {analysis_dir}")
                
                # Get filename with default path including analysis type
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                default_filename = os.path.join(analysis_dir, f"{analysis_type}_analysis_{timestamp}.txt")
                
                print(f"📁 Default save location: {os.path.abspath(default_filename)}")
                filename = input(f"Enter filename or press Enter for default: ").strip()
                
                if not filename:
                    filename = default_filename
                else:
                    # If user provides relative path, make it relative to analysis directory
                    if not os.path.isabs(filename) and not filename.startswith('.'):
                        filename = os.path.join(analysis_dir, filename)
                
                save_results(result, filename)
            
            print(f"✅ {analysis_type.capitalize()} analysis completed!")
        else:
            print(f"❌ {analysis_type.capitalize()} analysis failed or timed out")
            if comprehensive_analysis:
                print("💡 You can try:")
                print("   - Running quick analysis instead")
                print("   - Using fewer stocks")
                print("   - Running with no timeout")
            else:
                print("💡 The analysis may have encountered connection issues")
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run interactive mode
        interactive_mode()
    else:
        # Arguments provided, run CLI mode
        main()