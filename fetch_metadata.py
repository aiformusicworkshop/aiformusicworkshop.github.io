"""Fetch author names from accepted papers from OpenReview."""
import json

import openreview
import getpass

VENUE = "NeurIPS.cc/2025/Workshop/AI4Music"

def main():
    """Main function to fetch author names of accepted papers."""
    # Prompt for OpenReview username (email) and password
    username = input("Your OpenReview username (email): ")
    password = getpass.getpass("Your OpenReview password: ")

    # Initialize an OpenReview client
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net",
        username=username,
        password=password
    )

    # Fetch all accepted papers
    accepted_papers = client.get_all_notes(content={"venueid": VENUE})

    # Create a dictionary to store the output
    out_dict = {}

    # Iterate over all the accepted papers
    for paper in accepted_papers:
        # Find the submission number
        sub_num = None
        for reader in paper.content['authors']['readers']:
            if "Submission" in reader:
                sub_num = int(reader.split("Submission")[1].split("/")[0])
        if sub_num is None:
            raise ValueError(f"Could not find submission number for paper ID {paper.id}")

        # Store the paper metadata in the output dictionary
        out_dict[sub_num] = {
            "id": paper.id,
            "track": paper.content["track"]["value"] if "track" in paper.content else "Paper Track",
            "title": paper.content['title']['value'].replace("\t", " "),
            "authors": ", ".join(paper.content["authors"]["value"]).replace("\t", " ")
        }

    # Write the output dictionary to a JSON file
    out_dict = dict(sorted(out_dict.items()))
    with open('papers.json', 'w', encoding='utf-8') as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
