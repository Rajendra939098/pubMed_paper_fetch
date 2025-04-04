import requests
import csv

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_and_filter_papers(query, max_results=10):
    """Fetch papers from PubMed using the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        print("No results found.")
        return []

    # Fetch paper details
    details_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    details_response = requests.get(DETAILS_URL, params=details_params)

    if details_response.status_code != 200:
        raise Exception(f"Failed to fetch details: {details_response.status_code}")

    details = details_response.json().get("result", {})

    papers = []
    for paper_id in paper_ids:
        paper_info = details.get(paper_id, {})
        papers.append({
            "PubmedID": paper_id,
            "Title": paper_info.get("title", "Unknown Title"),
            "Publication Date": paper_info.get("pubdate", "Unknown Date"),
            "Authors": paper_info.get("authors", []),
            "Company Affiliations": paper_info.get("source", "Unknown"),
            "Corresponding Author Email": "Unknown"  # Placeholder
        })

    return papers

def save_to_csv(papers, filename):
    """Save papers to a CSV file."""
    if not papers:
        print("No data to save.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Results saved to {filename}")
