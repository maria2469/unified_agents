from agents.agent import *
from crewai import Task

financial_report_task = Task(
    description=(
        """Retrieve and analyze financial reports and market data for the given stock symbol {symbol} 
        using the Yahoo Finance API. Extract key financial metrics and provide a structured assessment 
        of the company's financial health. The report should include:  
        - **Company Financials:** Revenue, net income, and key financial indicators.  
        - **Market Summary:** Overview of the company s market standing and recent trends.  
        - **Stock Price Insights:** Latest stock price data and historical performance.  
        If the user provides a query, tailor the analysis accordingly while maintaining a comprehensive 
        financial evaluation."""
    ),
    agent=financial_report_agent,
    expected_output=(
        """A structured financial summary containing:  
        - **Key Financial Metrics:** Revenue, profitability, and other financial indicators.  
        - **Market Performance Overview:** Trends, risks, and company standing in the industry.  
        - **Stock Price Data:** Latest stock price, historical trends, and relevant insights.  
        If a specific query is provided, include insights tailored to the user request while ensuring a 
        complete financial assessment."""
    )
)


investment_advisor_task = Task(
    description=(
        """Provide tailored investment recommendations for the given stock symbol {symbol}. 
        If a specific query is provided, incorporate it into your analysis. Otherwise, perform a comprehensive evaluation 
        by analyzing valuation metrics, historical performance, and current market trends. 
        Deliver actionable insights in a well-structured format to support informed investment decisions."""
    ),
    agent=investment_advisor_agent,
    expected_output=(
        """A structured analysis that includes tailored investment recommendations, 
        a detailed review of valuation metrics, historical performance, current market trends, 
        and, if applicable, responses to any specific query provided."""
    )
)

query_answerer_task_financial = Task(
    description=(
        """Answer specific queries related to financial data, market trends, and investment opportunities for the company {symbol}.
        Utilize your expertise to provide accurate and detailed responses to user questions."""
    ),
    agent=query_answerer_agent_financial,
    expected_output=(
        """Accurate and detailed responses to user queries related to financial data, market trends, and investment opportunities."""
    )
)

research_task = Task(
    description=("Search news about {topic}"),
    agent=news_researcher ,
    expected_output=(" A list of news articles about {topic} with the title, url, image and snippet")

)

reporting_task = Task(
    description=("Generate a report on the {topic}"),
    agent=reporting_analyst,
    expected_output=("""    A fully fledge reporting of the news articles.  Make sure you have the title, summary, url and the image.
    Formatted as markdown without '```
                     """)
)

# stock_market_task = Task(
#     description=(
#         """Retrieve stock market data for the given stock symbol {symbol} using the function {function} from the Alpha Vantage API. 
#         Additionally, fetch global market open/close status to provide a broader market analysis. 
#         If a specific query is provided, tailor your insights accordingly. Otherwise, generate a structured summary that includes:  
#         - **Stock Performance:** Daily adjusted data for the requested stock.  
#         - **Market Status:** Current global market open/close status.  
#         - **Overall Insights:** A well-rounded evaluation of the stock's performance in relation to global market conditions."""
#     ),
#     agent=stock_market_agent,
#     expected_output=(
#         """A comprehensive report that includes:  
#         - **Detailed Stock Data:** Time-series financial data, including adjusted closing prices, volume, and trends.  
#         - **Market Status Overview:** The global market's open/close status to provide context on overall trading conditions.  
#         - **Actionable Insights:** A structured analysis of how the stock is performing in relation to market conditions.  
#         If a specific query is provided, include tailored insights addressing the query while ensuring a complete stock market evaluation."""
#     )
# )



medical_task = Task(
    description=(
        """Retrieve medical research data from PubMed using E-utilities based on the search term {term} and fetch up to {retmax} articles.  
        If a specific query is provided, generate a **detailed response** by leveraging expert-level medical knowledge  
        while incorporating relevant insights from the retrieved articles.  
        If no query is provided, conduct a **comprehensive analysis** of the abstracts, summarizing key findings,  
        medical implications, and recommendations in a well-structured format."""
    ),
    agent=medical_agent,
    expected_output=(
        """A detailed medical report including:  
        - **If a query is provided:** A **well-explained, expert-level response** addressing the query,  
          enriched with relevant research findings.  
        - **If no query is given:** A **structured summary** of retrieved PubMed abstracts,  
          highlighting key insights, medical implications, and expert recommendations.  
        
        The output should be **clear, structured, and informative**, making complex medical data easy to understand."""
    )
)
medical_query_answerer_task = Task(
    description=(
        """Retrieve and analyze medical research articles related to a given search term.  
        The agent will provide a general response based on existing medical knowledge  
        and enhance it with insights from relevant PubMed abstracts."""
    ),
    agent=medical_query_response_agent,
    expected_output=(
        """A structured response including:  
        - A general overview of the medical topic based on known information.  
        - Key insights from relevant research articles, including study findings or summaries.  
        - Citations or references to the retrieved abstracts for credibility."""
    )
)
