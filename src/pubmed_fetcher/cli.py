import argparse
from .fetch import fetch_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Save results to a file (CSV)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()

    try:
        papers = fetch_papers(args.query)
        if args.debug:
            print(papers)

        if args.file:
            save_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
