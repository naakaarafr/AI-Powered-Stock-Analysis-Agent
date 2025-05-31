"""
Tools module for the Stock Analysis CrewAI project.
Contains all custom tools for financial analysis and SEC data retrieval.
"""
import os
import requests
import json
import re
import html2text
from typing import Optional, Dict, Any, List, Type
from crewai_tools import tool, SerperDevTool, RagTool
from pydantic import BaseModel, Field
from embedchain.models.data_type import DataType
from config import config

# Import SEC API if available
try:
    from sec_api import QueryApi
    SEC_API_AVAILABLE = True
except ImportError:
    print("Warning: sec_api not installed. SEC tools will not work.")
    SEC_API_AVAILABLE = False

# Initialize search tool
def get_search_tool():
    """Get configured search tool."""
    try:
        if config.serper_api_key:
            return SerperDevTool(
                search_url="https://google.serper.dev/search",
                n_results=10
            )
        else:
            print("Warning: SERPER_API_KEY not found. Search tool unavailable.")
            return None
    except Exception as e:
        print(f"Error initializing search tool: {e}")
        return None

@tool("Financial Calculator")
def financial_calculator(operation: str) -> str:
    """
    Performs financial calculations including percentages, ratios, and basic math.
    
    Args:
        operation (str): Mathematical expression to evaluate (e.g., "100 * 0.15", "(500-400)/400*100")
    
    Returns:
        str: Result of the calculation or error message
    """
    try:
        # Safety check to prevent code execution
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in operation):
            return "Error: Invalid characters in expression. Only numbers, +, -, *, /, ., (, ), and spaces allowed."
        
        # Additional safety checks
        dangerous_patterns = ['__', 'import', 'exec', 'eval', 'open', 'file']
        if any(pattern in operation.lower() for pattern in dangerous_patterns):
            return "Error: Potentially dangerous operation detected"
        
        # Evaluate the mathematical expression
        result = eval(operation)
        return f"Calculation: {operation} = {result}"
        
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid mathematical expression syntax"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

@tool("Stock Price Analysis")
def analyze_stock_metrics(stock_data: str) -> str:
    """
    Analyze basic stock metrics and ratios from provided data.
    
    Args:
        stock_data (str): Stock data in format "price=100,volume=1000000,market_cap=5000000000"
    
    Returns:
        str: Analysis of the stock metrics
    """
    try:
        # Parse the stock data
        data = {}
        for item in stock_data.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = float(value.strip())
        
        analysis = "Stock Metrics Analysis:\n"
        
        if 'price' in data:
            analysis += f"- Current Price: ${data['price']:.2f}\n"
        
        if 'volume' in data:
            analysis += f"- Trading Volume: {data['volume']:,.0f}\n"
        
        if 'market_cap' in data:
            analysis += f"- Market Cap: ${data['market_cap']:,.0f}\n"
        
        # Calculate some basic ratios if we have the data
        if 'price' in data and 'earnings_per_share' in data and data['earnings_per_share'] > 0:
            pe_ratio = data['price'] / data['earnings_per_share']
            analysis += f"- P/E Ratio: {pe_ratio:.2f}\n"
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing stock data: {str(e)}"

# Schema classes for SEC tools
class SEC10KToolSchema(BaseModel):
    """Input schema for SEC 10-K tool."""
    search_query: str = Field(
        ...,
        description="Query to search within the 10-K report content",
    )

class SEC10QToolSchema(BaseModel):
    """Input schema for SEC 10-Q tool."""
    search_query: str = Field(
        ...,
        description="Query to search within the 10-Q report content",
    )

class SEC10KTool(RagTool):
    """Tool for searching within SEC 10-K filings."""
    
    name: str = "Search SEC 10-K Filing"
    description: str = "Search within a company's latest 10-K SEC filing for specific information."
    args_schema: Type[BaseModel] = SEC10KToolSchema

    def __init__(self, stock_name: str, **kwargs):
        """Initialize the SEC 10-K tool for a specific stock."""
        if not SEC_API_AVAILABLE:
            raise ImportError("sec_api package required. Install with: pip install sec-api")
        
        super().__init__(**kwargs)
        self.stock_name = stock_name.upper()
        
        print(f"Initializing SEC 10-K tool for {self.stock_name}")
        content = self._get_10k_content()
        if content:
            self.add(content)
            self.description = f"Search within {self.stock_name}'s latest 10-K SEC filing content."
        else:
            print(f"Warning: Could not retrieve 10-K content for {self.stock_name}")

    def _get_10k_content(self) -> Optional[str]:
        """Fetch and clean the latest 10-K filing content."""
        try:
            if not config.sec_api_key:
                print("Error: SEC_API_API_KEY not configured")
                return None
            
            query_api = QueryApi(api_key=config.sec_api_key)
            
            # Query for latest 10-K filing
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{self.stock_name} AND formType:\"10-K\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            
            filings_response = query_api.get_filings(query)
            filings = filings_response.get('filings', [])
            
            if not filings:
                print(f"No 10-K filings found for ticker: {self.stock_name}")
                return None

            filing_url = filings[0]['linkToFilingDetails']
            print(f"Found 10-K filing: {filing_url}")
            
            # Fetch the filing content
            headers = {
                "User-Agent": "Investment Analysis Tool contact@example.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            
            response = requests.get(filing_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Convert HTML to text
            html_converter = html2text.HTML2Text()
            html_converter.ignore_links = True
            html_converter.ignore_images = True
            text_content = html_converter.handle(response.content.decode("utf-8"))
            
            # Clean the text
            cleaned_text = re.sub(r'[^\w\s\.\,\;\:\!\?\$\%\(\)\-\+\=\[\]\"\'\/\\]', ' ', text_content)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            print(f"Successfully processed 10-K content ({len(cleaned_text)} characters)")
            return cleaned_text
            
        except Exception as e:
            print(f"Error fetching 10-K content: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        """Add content to the RAG system."""
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> str:
        """Execute the search query."""
        try:
            result = super()._run(query=search_query, **kwargs)
            return str(result) if result else "No relevant information found in the 10-K filing."
        except Exception as e:
            return f"Error searching 10-K filing: {str(e)}"

class SEC10QTool(RagTool):
    """Tool for searching within SEC 10-Q filings."""
    
    name: str = "Search SEC 10-Q Filing"
    description: str = "Search within a company's latest 10-Q SEC filing for specific information."
    args_schema: Type[BaseModel] = SEC10QToolSchema

    def __init__(self, stock_name: str, **kwargs):
        """Initialize the SEC 10-Q tool for a specific stock."""
        if not SEC_API_AVAILABLE:
            raise ImportError("sec_api package required. Install with: pip install sec-api")
        
        super().__init__(**kwargs)
        self.stock_name = stock_name.upper()
        
        print(f"Initializing SEC 10-Q tool for {self.stock_name}")
        content = self._get_10q_content()
        if content:
            self.add(content)
            self.description = f"Search within {self.stock_name}'s latest 10-Q SEC filing content."
        else:
            print(f"Warning: Could not retrieve 10-Q content for {self.stock_name}")

    def _get_10q_content(self) -> Optional[str]:
        """Fetch and clean the latest 10-Q filing content."""
        try:
            if not config.sec_api_key:
                print("Error: SEC_API_API_KEY not configured")
                return None
            
            query_api = QueryApi(api_key=config.sec_api_key)
            
            # Query for latest 10-Q filing
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{self.stock_name} AND formType:\"10-Q\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            
            filings_response = query_api.get_filings(query)
            filings = filings_response.get('filings', [])
            
            if not filings:
                print(f"No 10-Q filings found for ticker: {self.stock_name}")
                return None

            filing_url = filings[0]['linkToFilingDetails']
            print(f"Found 10-Q filing: {filing_url}")
            
            # Fetch the filing content
            headers = {
                "User-Agent": "Investment Analysis Tool contact@example.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            
            response = requests.get(filing_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Convert HTML to text
            html_converter = html2text.HTML2Text()
            html_converter.ignore_links = True
            html_converter.ignore_images = True
            text_content = html_converter.handle(response.content.decode("utf-8"))
            
            # Clean the text
            cleaned_text = re.sub(r'[^\w\s\.\,\;\:\!\?\$\%\(\)\-\+\=\[\]\"\'\/\\]', ' ', text_content)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            print(f"Successfully processed 10-Q content ({len(cleaned_text)} characters)")
            return cleaned_text
            
        except Exception as e:
            print(f"Error fetching 10-Q content: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        """Add content to the RAG system."""
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> str:
        """Execute the search query."""
        try:
            result = super()._run(query=search_query, **kwargs)
            return str(result) if result else "No relevant information found in the 10-Q filing."
        except Exception as e:
            return f"Error searching 10-Q filing: {str(e)}"

# Utility functions
def create_sec_tools(stock_symbols: List[str]) -> Dict[str, List]:
    """
    Create SEC tools for multiple stocks.
    
    Args:
        stock_symbols: List of stock ticker symbols
        
    Returns:
        Dictionary with '10k_tools' and '10q_tools' lists
    """
    tools = {"10k_tools": [], "10q_tools": []}
    
    for symbol in stock_symbols:
        try:
            # Create 10-K tool
            tool_10k = SEC10KTool(stock_name=symbol)
            tools["10k_tools"].append(tool_10k)
            print(f"✅ Created 10-K tool for {symbol}")
        except Exception as e:
            print(f"❌ Failed to create 10-K tool for {symbol}: {e}")
        
        try:
            # Create 10-Q tool
            tool_10q = SEC10QTool(stock_name=symbol)
            tools["10q_tools"].append(tool_10q)
            print(f"✅ Created 10-Q tool for {symbol}")
        except Exception as e:
            print(f"❌ Failed to create 10-Q tool for {symbol}: {e}")
    
    return tools

# Create tool instances and export them
def get_available_tools():
    """Get list of available tools."""
    tools = []
    
    # Add basic tools
    tools.append(financial_calculator)
    tools.append(analyze_stock_metrics)
    
    # Add search tool if available
    search_tool = get_search_tool()
    if search_tool:
        tools.append(search_tool)
    
    return tools

# Function to test if tools are callable
def test_tools():
    """Test that all tools are properly callable."""
    tools = get_available_tools()
    
    for tool in tools:
        try:
            # Check if tool has the required methods
            if hasattr(tool, '_run') or hasattr(tool, '__call__'):
                print(f"✅ Tool {getattr(tool, 'name', type(tool).__name__)} is properly configured")
            else:
                print(f"❌ Tool {getattr(tool, 'name', type(tool).__name__)} is missing _run or __call__ method")
        except Exception as e:
            print(f"❌ Error testing tool {getattr(tool, 'name', type(tool).__name__)}: {e}")
    
    # Test SEC tools if available
    if SEC_API_AVAILABLE and config.sec_api_key:
        try:
            sec_tools = create_sec_tools(['AAPL'])
            for tool_type, tool_list in sec_tools.items():
                for tool in tool_list:
                    if hasattr(tool, '_run'):
                        print(f"✅ SEC tool {tool.name} is properly configured")
                    else:
                        print(f"❌ SEC tool {tool.name} is missing _run method")
        except Exception as e:
            print(f"❌ Error testing SEC tools: {e}")

# Export available tools
available_tools = get_available_tools()

# Add a test when the module is run directly
if __name__ == "__main__":
    test_tools()