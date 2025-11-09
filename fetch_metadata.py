"""Fetch all author names from OpenReview."""
import argparse
import json
import pathlib

import getpass
import openreview

VENUE = "NeurIPS.cc/2025/Workshop/AI4Music"

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch all author names from OpenReview.")
    parser.add_argument("-o", "--out_file", type=pathlib.Path, default="papers.json")
    return parser.parse_args()

def main():
    """Fetch all author names from OpenReview."""
    # Parse command-line arguments
    args = parse_args()

    # Prompt for OpenReview username (email) and password
    username = input("Your OpenReview username (email): ")
    password = getpass.getpass("Your OpenReview password: ")

    # Initialize an OpenReview client
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net",
        username=username,
        password=password
    )

    # Fetch all papers
    papers = client.get_all_notes(content={"venueid": VENUE})

    # Create a dictionary to store the output
    out_dict = {}

    # Iterate over all the papers
    for paper in papers:
        # Store the paper metadata in the output dictionary
        out_dict[paper.number] = {
            "id": paper.id,
            "track": paper.content["track"]["value"] if "track" in paper.content else "Paper Track",
            "title": paper.content["title"]["value"].replace("\t", " "),
            "authors": ", ".join(paper.content["authors"]["value"]).replace("\t", " "),
            "forum": f"https://openreview.net/forum?id={paper.id}",
            "pdf": f"https://openreview.net/pdf?id={paper.id}",
        }
        if "video_link" in paper.content:
            out_dict[paper.number]["video"] = paper.content["video_link"]["value"]
        elif "video_file" in paper.content:
            out_dict[paper.number]["video"] = f"https://openreview.net/attachment?id={paper.id}&name=video_file"

    # Write the output dictionary to a JSON file
    out_dict = dict(sorted(out_dict.items()))
    with open(args.out_file, "w", encoding="utf-8") as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
