# pubmed_fetcher/cli.py

import argparse
import logging
from .fetch import fetch_and_filter_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    results = fetch_and_filter_papers(args.query)
    

    if args.file:
        save_to_csv(results, args.file)
    else:
        for paper in results:
            print(paper)

if __name__ == "__main__":
    main()
