"""Extract authors from papers.json and save to authors.txt."""

import json

def main():
    """Extract authors from papers.json and save to authors.txt."""
    with open("authors_paper.txt", "w", encoding="utf-8") as out_file_paper:
        with open("authors_demo.txt", "w", encoding="utf-8") as out_file_demo:
            with open("_data/papers.json", "r", encoding="utf-8") as file:
                papers = json.load(file)
                for _, meta in papers.items():
                    if meta["track"] == "Paper Track":
                        out_file_paper.write(meta["authors"] + '\n')
                    elif meta["track"] == "Demo Track":
                        out_file_demo.write(meta["authors"] + '\n')
                    else:
                        raise ValueError(f"Unknown track: {meta['track']}")

if __name__ == '__main__':
    main()
