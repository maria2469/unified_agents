from crewai.tools import tool,BaseTool
import requests
import os
from yahooquery import Ticker
from newsapi import NewsApiClient
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json

from dotenv import load_dotenv

load_dotenv()

class CustomSerperDevTool(BaseTool):
    name: str = "Custom Serper Dev Tool"
    description: str = "Search the internet for news."

    def _run(self, query: str) -> str:
        """
        Search the internet for news.
        """

        url = "https://google.serper.dev/news"

        payload = json.dumps({
            "q": query,
            "num": 20,
            "autocorrect": False,
            "tbs": "qdr:d"
        })

        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Parse the JSON response
        response_data = response.json()

        # Extract only the 'news' property
        news_data = response_data.get('news', [])

        # Convert the news data back to a JSON string
        return json.dumps(news_data, indent=2)
    

@tool("get financial reports and market data")
def fetch_financial_reports(symbol: str):
    """
    Fetches financial reports and market data for a given stock symbol using Yahoo Finance API.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple).
    
    Returns:
        dict: A dictionary containing financial reports and market data.
    """
    try:
        ticker = Ticker(symbol)
        data = {
            "financials": ticker.financial_data,
            "summary": ticker.summary_detail,
            "price": ticker.price
        }
        return data
    except Exception as e:
        return {"error": str(e)}
    
@tool("fetch investment analysis")
def fetch_investment_analysis(symbol: str):
    """
    Fetches investment analysis data for a given stock symbol using various financial APIs.
    
    Args:
        symbol (str): The stock symbol (e.g., 'GOOGL' for Alphabet Inc.).
    
    Returns:
        dict: A dictionary containing analysis data such as valuation metrics, historical performance,
              and analyst recommendations.
    """
    try:
        ticker = Ticker(symbol)
        data = {
            "valuation": ticker.valuation_measures,
            "performance": ticker.earning_history,
            "analystRecommendations": ticker.recommendation_trend
        }
        return data
    except Exception as e:
        return {"error": str(e)}

# alpha_van_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# @tool("get financial reports and market data from Alpha Vantage")
# def fetch_alpha_vantage_data(symbol: str, function: str = "TIME_SERIES_DAILY_ADJUSTED"):
#     """
#     Fetches financial reports and market data from Alpha Vantage.

#     Args:
#         symbol (str): Stock symbol (e.g., 'AAPL' for Apple).
#         function (str): API function (default is "TIME_SERIES_DAILY_ADJUSTED").

#     Returns:
#         dict: JSON response from Alpha Vantage API.
#     """
#     try:
#         url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={alpha_van_api_key}"
#         response = requests.get(url)
#         data = response.json()
#         return data
#     except Exception as e:
#         return {"error": str(e)}
    
# @tool("get market global open and close status")
# def get_market_status(function : str = "GLOBAL_MARKET"):
#     """
#     Fetches Global market open and close status data from Alpha Vantage.
#     """

#     try:
#         url = f'https://www.alphavantage.co/query?{function}=MARKET_STATUS&apikey={alpha_van_api_key}'
#         response = requests.get(url)
#         data = response.json()
#         return data
#     except Exception as e:
#         return {"error": str(e)}
    



@tool("fetch data of medical articles")
def fetch_data(term: str, retmax: str = "2"):
    """
    Fetches abstracts of medical articles from PubMed based on a search term.
    
    This function uses NCBI's E-utilities to first search for article IDs matching the term
    and then fetches their abstracts.
    
    Args:
        trm (str): The search term for querying medical articles.
        retm (str): The maximum number of article IDs to retrieve.
    
    Returns:
        str or dict: A string containing the abstracts of the fetched articles, or a dict with an error message.
    """
    # Define the URL and parameters for the ESearch endpoint.
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "pubmed",
        "term": term,
        "retmax": retmax,
        "retmode": "json"
    }
    
    try:
        # Execute the ESearch request.
        esearch_response = requests.get(esearch_url, params=esearch_params)
        esearch_data = esearch_response.json()
        
        # Extract the list of article IDs from the JSON response.
        article_ids = esearch_data.get("esearchresult", {}).get("idlist", [])
        if not article_ids:
            return {"error": "No articles found for the given search term."}
        
        # Join the article IDs into a comma-separated string.
        ids_str = ",".join(article_ids)
        
        # Define the URL and parameters for the EFetch endpoint.
        efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        efetch_params = {
            "db": "pubmed",
            "id": ids_str,
            "retmode": "text",
            "rettype": "abstract"
        }
        
        # Execute the EFetch request.
        efetch_response = requests.get(efetch_url, params=efetch_params)
        
        # Return the fetched abstracts as plain text.
        return efetch_response.text
        
    except Exception as e:
        return {"error": f"Failed to fetch medical data: {str(e)}"}

