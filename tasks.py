"""
Tasks module for the Stock Analysis CrewAI project.
Defines specialized tasks for different aspects of financial analysis.
"""
from crewai import Task
from textwrap import dedent

class FinancialTasks:
    """Factory class for creating financial analysis tasks."""
    
    @staticmethod
    def create_research_task(agent, stocks: str, focus_areas: str = "comprehensive analysis") -> Task:
        """Create a comprehensive research task."""
        return Task(
            description=dedent(f"""
                **COMPREHENSIVE STOCK RESEARCH TASK**

                Conduct thorough research and analysis on the specified stocks to gather all relevant 
                information needed for investment decision-making.

                **Research Scope:**
                - Company fundamentals (revenue, earnings, growth trends, margins)
                - Financial health indicators (debt levels, cash flow, liquidity)
                - Industry analysis and competitive positioning
                - Recent news, earnings reports, and market developments
                - Management quality and corporate governance
                - Business model and competitive advantages
                - Key risks and challenges facing each company

                **Research Process:**
                1. Gather financial data from recent quarterly and annual reports
                2. Analyze industry trends and competitive landscape
                3. Review recent news and analyst coverage
                4. Assess management effectiveness and strategic direction
                5. Identify key growth drivers and risk factors
                6. Compare companies against industry peers

                **Target Stocks:** {stocks}
                **Focus Areas:** {focus_areas}

                **Deliverable:**
                Provide a detailed research report for each stock that includes:
                - Executive summary of investment thesis
                - Key financial metrics and trends
                - Competitive position and market dynamics
                - Major opportunities and risks
                - Recent developments and news impact
            """),
            agent=agent,
            expected_output="""A comprehensive research report containing:
            - Executive summary for each stock analyzed
            - Key financial metrics, ratios, and performance trends
            - Industry and competitive analysis
            - Identification of growth drivers and risk factors
            - Summary of recent developments and their potential impact
            - Clear data-driven insights to support investment decisions"""
        )
    
    @staticmethod
    def create_financial_analysis_task(agent, stocks: str, analysis_focus: str = "valuation and financial health") -> Task:
        """Create a detailed financial analysis task."""
        return Task(
            description=dedent(f"""
                **DETAILED FINANCIAL ANALYSIS TASK**

                Perform in-depth financial analysis of the specified stocks, focusing on valuation, 
                financial health, and investment attractiveness.

                **Analysis Requirements:**
                1. **Valuation Analysis:**
                   - P/E, P/B, P/S, EV/EBITDA ratios
                   - Comparison with industry averages and historical ranges
                   - DCF analysis considerations
                   - Relative valuation vs. peers

                2. **Financial Health Assessment:**
                   - Profitability metrics (margins, ROE, ROA, ROIC)
                   - Liquidity ratios (current ratio, quick ratio)
                   - Leverage ratios (debt-to-equity, interest coverage)
                   - Cash flow analysis (operating, free cash flow)

                3. **Growth Analysis:**
                   - Revenue and earnings growth trends
                   - Margin expansion/contraction patterns
                   - Capital allocation efficiency
                   - Reinvestment rates and returns

                4. **Quality Metrics:**
                   - Earnings quality and consistency
                   - Balance sheet strength
                   - Cash conversion and working capital management

                **Target Stocks:** {stocks}
                **Analysis Focus:** {analysis_focus}

                **Deliverable:**
                Provide a detailed financial analysis report with clear investment implications.
            """),
            agent=agent,
            expected_output="""A detailed financial analysis report containing:
            - Comprehensive valuation assessment with multiple metrics
            - Financial health evaluation with key ratios and trends
            - Growth analysis and sustainability assessment
            - Quality metrics and red flag identification
            - Comparative analysis against industry peers
            - Clear conclusions on financial attractiveness and fair value estimates"""
        )
    
    @staticmethod
    def create_investment_recommendation_task(agent, stocks: str, investor_profile: dict) -> Task:
        """Create an investment recommendation task."""
        
        goals = investor_profile.get('goals', 'wealth building')
        risk_tolerance = investor_profile.get('risk_tolerance', 'moderate')
        investment_horizon = investor_profile.get('investment_horizon', 'long-term')
        investment_amount = investor_profile.get('investment_amount', 'not specified')
        
        return Task(
            description=dedent(f"""
                **INVESTMENT RECOMMENDATION TASK**

                Based on the comprehensive research and financial analysis, provide personalized 
                investment recommendations that align with the investor's profile and objectives.

                **Recommendation Process:**
                1. **Portfolio Fit Assessment:**
                   - Alignment with investor goals and risk tolerance
                   - Diversification benefits
                   - Time horizon suitability
                   - Position sizing considerations

                2. **Risk-Return Analysis:**
                   - Potential upside and downside scenarios
                   - Risk factors and mitigation strategies
                   - Volatility expectations
                   - Correlation with existing holdings (if applicable)

                3. **Strategic Recommendations:**
                   - Top pick(s) with detailed rationale
                   - Entry timing and price targets
                   - Position sizing recommendations
                   - Exit strategies and stop-loss levels

                4. **Alternative Considerations:**
                   - Sector/thematic alternatives
                   - Risk-adjusted alternatives
                   - Diversification suggestions

                **Investor Profile:**
                - Investment Goals: {goals}
                - Risk Tolerance: {risk_tolerance}  
                - Investment Horizon: {investment_horizon}
                - Investment Amount: {investment_amount}
                - Target Stocks: {stocks}

                **Deliverable:**
                Provide clear, actionable investment recommendations with specific rationale.
            """),
            agent=agent,
            expected_output="""A personalized investment recommendation report containing:
            - Top stock recommendation with detailed investment thesis
            - Clear rationale based on research and analysis findings
            - Risk assessment and alignment with investor profile
            - Specific entry strategies and price targets
            - Position sizing and portfolio allocation suggestions
            - Key catalysts and timeline expectations
            - Risk management and exit strategy recommendations
            - Alternative investment options if primary recommendation doesn't fit"""
        )
    
    @staticmethod
    def create_market_analysis_task(agent, stocks: str, market_focus: str = "current market conditions") -> Task:
        """Create a market and sector analysis task."""
        return Task(
            description=dedent(f"""
                **MARKET AND SECTOR ANALYSIS TASK**

                Analyze current market conditions, sector dynamics, and macroeconomic factors 
                that could impact the specified stocks and overall investment strategy.

                **Analysis Requirements:**
                1. **Market Environment Assessment:**
                   - Current market trends and sentiment
                   - Key economic indicators and their implications
                   - Interest rate environment and monetary policy impact
                   - Market volatility and risk appetite

                2. **Sector Analysis:**
                   - Industry trends and growth prospects
                   - Regulatory environment and policy changes
                   - Competitive dynamics and market share shifts
                   - Technological disruptions and innovations

                3. **Timing Considerations:**
                   - Market cycle positioning
                   - Seasonal and cyclical factors
                   - Upcoming catalysts and events
                   - Technical analysis and chart patterns

                4. **Risk Assessment:**
                   - Systemic risks and market correlations
                   - Geopolitical and economic uncertainties
                   - Sector-specific risks and challenges
                   - Liquidity and market structure considerations

                **Target Stocks:** {stocks}
                **Market Focus:** {market_focus}

                **Deliverable:**
                Provide comprehensive market context for investment decisions.
            """),
            agent=agent,
            expected_output="""A comprehensive market analysis report containing:
            - Current market environment assessment and outlook
            - Detailed sector analysis and industry dynamics
            - Identification of key market drivers and catalysts
            - Risk factor analysis and potential market scenarios
            - Timing recommendations and technical insights
            - Strategic implications for the target stocks
            - Market-based recommendations for portfolio positioning"""
        )

def create_analysis_workflow(agents: dict, stocks: str, investor_profile: dict) -> list:
    """
    Create a complete workflow of tasks for stock analysis.
    
    Args:
        agents: Dictionary of agents created by create_financial_team()
        stocks: Comma-separated string of stock symbols
        investor_profile: Dictionary with investor details
        
    Returns:
        List of tasks in execution order
    """
    tasks = []
    
    # 1. Research Task
    research_task = FinancialTasks.create_research_task(
        agent=agents["research_analyst"],
        stocks=stocks,
        focus_areas="fundamental analysis, industry trends, competitive positioning"
    )
    tasks.append(research_task)
    
    # 2. Financial Analysis Task
    financial_task = FinancialTasks.create_financial_analysis_task(
        agent=agents["financial_analyst"],
        stocks=stocks,
        analysis_focus="valuation, financial health, growth prospects"
    )
    tasks.append(financial_task)
    
    # 3. Market Analysis Task
    market_task = FinancialTasks.create_market_analysis_task(
        agent=agents["market_strategist"],
        stocks=stocks,
        market_focus="current conditions, sector trends, timing considerations"
    )
    tasks.append(market_task)
    
    # 4. Investment Recommendation Task (depends on previous tasks)
    recommendation_task = FinancialTasks.create_investment_recommendation_task(
        agent=agents["investment_advisor"],
        stocks=stocks,
        investor_profile=investor_profile
    )
    tasks.append(recommendation_task)
    
    return tasks

def create_quick_analysis_workflow(agents: dict, stocks: str, investor_profile: dict) -> list:
    """
    Create a streamlined workflow for quick stock analysis.
    
    Args:
        agents: Dictionary of agents
        stocks: Stock symbols to analyze
        investor_profile: Investor details
        
    Returns:
        List of essential tasks for quick analysis
    """
    tasks = []
    
    # Combined Research and Analysis Task
    combined_task = Task(
        description=dedent(f"""
            **RAPID STOCK ANALYSIS TASK**
            
            Conduct a focused analysis of the specified stocks to provide quick investment insights.
            
            **Analysis Requirements:**
            1. Key financial metrics and recent performance
            2. Current valuation vs. historical and peer averages
            3. Major recent developments and news impact
            4. Primary investment thesis and key risks
            5. Alignment with investor profile and goals
            
            **Target Stocks:** {stocks}
            **Investor Profile:** {investor_profile}
            
            Focus on the most critical factors for investment decision-making.
        """),
        agent=agents["research_analyst"],
        expected_output="""A concise analysis report with:
        - Key financial highlights and valuation metrics
        - Investment thesis and primary risks for each stock
        - Quick assessment of fit with investor profile
        - Clear recommendation with rationale"""
    )
    tasks.append(combined_task)
    
    # Final Recommendation
    final_rec = FinancialTasks.create_investment_recommendation_task(
        agent=agents["investment_advisor"],
        stocks=stocks,
        investor_profile=investor_profile
    )
    tasks.append(final_rec)
    
    return tasks