"""
Agents module for the Stock Analysis CrewAI project.
Defines specialized agents for different aspects of financial analysis.
"""
from crewai import Agent
from config import config
from tools import available_tools

class FinancialAgents:
    """Factory class for creating financial analysis agents."""
    
    def __init__(self, additional_tools=None):
        """Initialize with base tools and optional additional tools."""
        self.llm = config.get_llm()
        self.base_tools = available_tools.copy()
        if additional_tools:
            self.base_tools.extend(additional_tools)
    
    def create_research_analyst(self) -> Agent:
        """Create a research analyst agent focused on data gathering and analysis."""
        return Agent(
            role="Senior Stock Research Analyst",
            goal="Conduct comprehensive research and analysis of stocks, gathering key financial data, market trends, and industry insights to support investment decisions",
            backstory="""
            You are a seasoned stock research analyst with over 15 years of experience in equity research.
            You have worked at top-tier investment banks and have a proven track record of identifying 
            profitable investment opportunities. You excel at:
            
            - Analyzing financial statements and SEC filings
            - Identifying market trends and industry dynamics
            - Conducting thorough fundamental analysis
            - Gathering and synthesizing information from multiple sources
            - Providing detailed, data-driven research reports
            
            You are methodical, detail-oriented, and always back your findings with solid evidence.
            """,
            tools=self.base_tools,
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
            max_execution_time=300
        )
    
    def create_financial_analyst(self) -> Agent:
        """Create a financial analyst agent focused on financial metrics and valuation."""
        return Agent(
            role="Expert Financial Analyst",
            goal="Analyze financial metrics, ratios, and valuation models to assess the financial health and investment attractiveness of stocks",
            backstory="""
            You are a highly skilled financial analyst with expertise in financial modeling and valuation.
            You have an MBA in Finance and CFA certification, with 12+ years of experience in financial analysis.
            Your specialties include:
            
            - Financial ratio analysis and interpretation
            - DCF modeling and relative valuation
            - Risk assessment and financial health evaluation
            - Earnings analysis and forecasting
            - Capital structure and debt analysis
            
            You have a keen eye for identifying red flags in financial statements and can quickly 
            assess whether a company is financially sound and fairly valued.
            """,
            tools=self.base_tools,
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
            max_execution_time=300
        )
    
    def create_investment_advisor(self) -> Agent:
        """Create an investment advisor agent focused on recommendations and strategy."""
        return Agent(
            role="Senior Investment Advisor",
            goal="Provide personalized investment recommendations and strategic advice based on comprehensive analysis and investor profile",
            backstory="""
            You are a senior investment advisor with 20+ years of experience managing portfolios for 
            high-net-worth individuals and institutions. You hold both CFA and CFP certifications and 
            have successfully navigated multiple market cycles. Your expertise includes:
            
            - Portfolio construction and asset allocation
            - Risk management and diversification strategies
            - Matching investments to client goals and risk tolerance
            - Market timing and entry/exit strategies
            - Behavioral finance and investor psychology
            
            You are known for your ability to translate complex financial analysis into clear, 
            actionable investment advice that aligns with each client's unique situation.
            """,
            tools=self.base_tools,
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
            max_execution_time=300
        )
    
    def create_market_strategist(self) -> Agent:
        """Create a market strategist agent focused on macro trends and market conditions."""
        return Agent(
            role="Chief Market Strategist",
            goal="Analyze macroeconomic conditions, market trends, and sector dynamics to provide strategic market insights and timing recommendations",
            backstory="""
            You are a chief market strategist with extensive experience in macroeconomic analysis and 
            market forecasting. You have worked at leading investment firms and have been quoted in 
            major financial publications. Your areas of expertise include:
            
            - Macroeconomic analysis and policy impact assessment
            - Market cycle analysis and timing
            - Sector rotation and thematic investing
            - Technical analysis and chart pattern recognition
            - Global market dynamics and correlation analysis
            
            You have a unique ability to synthesize complex macroeconomic data into actionable 
            investment themes and can identify when market conditions favor certain types of investments.
            """,
            tools=self.base_tools,
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
            max_execution_time=300
        )

# Convenience function to create a standard set of agents
def create_financial_team(additional_tools=None) -> dict:
    """
    Create a complete team of financial analysis agents.
    
    Args:
        additional_tools: Optional list of additional tools to provide to agents
        
    Returns:
        Dictionary containing all created agents
    """
    agent_factory = FinancialAgents(additional_tools)
    
    return {
        "research_analyst": agent_factory.create_research_analyst(),
        "financial_analyst": agent_factory.create_financial_analyst(),
        "investment_advisor": agent_factory.create_investment_advisor(),
        "market_strategist": agent_factory.create_market_strategist()
    }