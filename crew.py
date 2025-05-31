"""
Crew module for the Stock Analysis CrewAI project.
Orchestrates the complete stock analysis workflow.
"""
from crewai import Crew, Process
from typing import List, Dict, Optional
from agents import create_financial_team
from tasks import create_analysis_workflow, create_quick_analysis_workflow
from tools import create_sec_tools
from config import config

class StockAnalysisCrew:
    """Main crew orchestrator for stock analysis."""
    
    def __init__(self, stocks: List[str], enable_sec_tools: bool = False):
        """
        Initialize the stock analysis crew.
        
        Args:
            stocks: List of stock ticker symbols to analyze
            enable_sec_tools: Whether to enable SEC filing analysis tools
        """
        self.stocks = stocks
        self.stock_string = ", ".join(stocks)
        self.enable_sec_tools = enable_sec_tools
        self.agents = None
        self.sec_tools = None
        
        # Display configuration
        config.display_status()
        
        # Initialize components
        self._setup_tools()
        self._setup_agents()
    
    def _setup_tools(self):
        """Setup additional tools including SEC tools if enabled."""
        self.additional_tools = []
        
        if self.enable_sec_tools and len(self.stocks) > 0:
            try:
                print(f"🔧 Setting up SEC tools for stocks: {self.stock_string}")
                self.sec_tools = create_sec_tools(self.stocks)
                
                # Add SEC tools to additional tools list
                if self.sec_tools["10k_tools"]:
                    self.additional_tools.extend(self.sec_tools["10k_tools"])
                if self.sec_tools["10q_tools"]:
                    self.additional_tools.extend(self.sec_tools["10q_tools"])
                    
                print(f"✅ SEC tools setup complete: {len(self.additional_tools)} tools created")
            except Exception as e:
                print(f"⚠️ SEC tools setup failed: {e}")
                print("Continuing without SEC tools...")
    
    def _setup_agents(self):
        """Setup the agent team."""
        print("🤖 Setting up financial analysis agents...")
        self.agents = create_financial_team(self.additional_tools)
        print("✅ Agent team ready")
    
    def analyze_stocks(self, investor_profile: Dict, quick_analysis: bool = False) -> str:
        """
        Perform comprehensive stock analysis.
        
        Args:
            investor_profile: Dictionary containing investor details
            quick_analysis: Whether to use quick analysis workflow
            
        Returns:
            Analysis results as string
        """
        try:
            print(f"📊 Starting {'quick' if quick_analysis else 'comprehensive'} analysis...")
            print(f"📈 Analyzing stocks: {self.stock_string}")
            print(f"👤 Investor profile: {investor_profile}")
            
            # Create appropriate task workflow
            if quick_analysis:
                tasks = create_quick_analysis_workflow(
                    agents=self.agents,
                    stocks=self.stock_string,
                    investor_profile=investor_profile
                )
            else:
                tasks = create_analysis_workflow(
                    agents=self.agents,
                    stocks=self.stock_string,
                    investor_profile=investor_profile
                )
            
            # Create and execute crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                memory=True,
                max_execution_time=1800  # 30 minutes max
            )
            
            print("🚀 Executing analysis workflow...")
            result = crew.kickoff()
            
            print("✅ Analysis completed successfully!")
            return str(result)
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_stock_recommendation(self, investor_profile: Dict) -> str:
        """
        Get a focused stock recommendation.
        
        Args:
            investor_profile: Investor details and preferences
            
        Returns:
            Investment recommendation as string
        """
        try:
            print(f"🎯 Generating recommendation for: {self.stock_string}")
            
            # Use investment advisor for focused recommendation
            from tasks import FinancialTasks
            
            recommendation_task = FinancialTasks.create_investment_recommendation_task(
                agent=self.agents["investment_advisor"],
                stocks=self.stock_string,
                investor_profile=investor_profile
            )
            
            crew = Crew(
                agents=[self.agents["investment_advisor"]],
                tasks=[recommendation_task],
                process=Process.sequential,
                verbose=True,
                max_execution_time=600  # 10 minutes max
            )
            
            result = crew.kickoff()
            print("✅ Recommendation generated!")
            return str(result)
            
        except Exception as e:
            error_msg = f"❌ Recommendation failed: {str(e)}"
            print(error_msg)
            return error_msg

class StockAnalysisManager:
    """High-level manager for stock analysis operations."""
    
    @staticmethod
    def create_analysis_session(
        stocks: List[str],
        investor_profile: Dict,
        enable_sec_tools: bool = False,
        quick_analysis: bool = False
    ) -> str:
        """
        Create and run a complete stock analysis session.
        
        Args:
            stocks: List of stock symbols to analyze
            investor_profile: Investor details
            enable_sec_tools: Enable SEC filing analysis
            quick_analysis: Use quick analysis workflow
            
        Returns:
            Analysis results
        """
        try:
            # Validate inputs
            if not stocks:
                return "❌ Error: No stocks provided for analysis"
            
            if not investor_profile:
                return "❌ Error: Investor profile is required"
            
            # Create crew and run analysis
            crew = StockAnalysisCrew(stocks=stocks, enable_sec_tools=enable_sec_tools)
            result = crew.analyze_stocks(investor_profile=investor_profile, quick_analysis=quick_analysis)
            
            return result
            
        except Exception as e:
            return f"❌ Session failed: {str(e)}"
    
    @staticmethod
    def get_quick_recommendation(stocks: List[str], investor_profile: Dict) -> str:
        """
        Get a quick stock recommendation.
        
        Args:
            stocks: Stock symbols to evaluate
            investor_profile: Investor details
            
        Returns:
            Investment recommendation
        """
        try:
            crew = StockAnalysisCrew(stocks=stocks, enable_sec_tools=False)
            return crew.get_stock_recommendation(investor_profile=investor_profile)
        except Exception as e:
            return f"❌ Quick recommendation failed: {str(e)}"

# Convenience functions for common use cases
def analyze_stocks_comprehensive(
    stocks: List[str],
    goals: str = "long-term growth",
    risk_tolerance: str = "moderate",
    investment_horizon: str = "5+ years",
    investment_amount: str = "$10,000"
) -> str:
    """Run comprehensive stock analysis with default investor profile."""
    investor_profile = {
        "goals": goals,
        "risk_tolerance": risk_tolerance,
        "investment_horizon": investment_horizon,
        "investment_amount": investment_amount
    }
    
    return StockAnalysisManager.create_analysis_session(
        stocks=stocks,
        investor_profile=investor_profile,
        enable_sec_tools=True,
        quick_analysis=False
    )

def analyze_stocks_quick(
    stocks: List[str],
    goals: str = "growth",
    risk_tolerance: str = "moderate"
) -> str:
    """Run quick stock analysis with minimal investor profile."""
    investor_profile = {
        "goals": goals,
        "risk_tolerance": risk_tolerance,
        "investment_horizon": "medium-term",
        "investment_amount": "not specified"
    }
    
    return StockAnalysisManager.create_analysis_session(
        stocks=stocks,
        investor_profile=investor_profile,
        enable_sec_tools=False,
        quick_analysis=True
    )