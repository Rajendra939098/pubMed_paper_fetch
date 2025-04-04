import requests
import pandas as pd
from typing import List, Dict

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from PubMed based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    
    response = requests.get(PUBMED_API_URL, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch results from PubMed.")
    
    data = response.json()
    pubmed_ids = data["esearchresult"]["idlist"]
    
    return fetch_details(pubmed_ids)

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch detailed information about papers using PubMed IDs."""
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    
    response = requests.get(DETAILS_API_URL, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch paper details.")
    
    data = response.json()
    papers = []
    
    for pid in pubmed_ids:
        if pid in data["result"]:
            details = data["result"][pid]
            papers.append({
                "PubmedID": pid,
                "Title": details.get("title", "N/A"),
                "Publication Date": details.get("pubdate", "N/A"),
                "Authors": [author.get("name", "Unknown") for author in details.get("authors", [])],
                "Company Affiliations": "Unknown",  # Need heuristic to detect
                "Corresponding Author Email": "Unknown"  # Need heuristic to detect
            })
    
    return papers

def save_to_csv(papers: List[Dict], filename: str = "papers.csv"):
    """Save fetched papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
