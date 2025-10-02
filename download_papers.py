"""Download all papers from OpenReview."""
import pathlib

import openreview
import getpass

VENUE = "NeurIPS.cc/2025/Workshop/AI4Music"

def main():
    """Download all papers from OpenReview."""
    # Make sure the output directory exists
    out_dir = pathlib.Path("papers")
    out_dir.mkdir(exist_ok=True)

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

    # Iterate over all the papers
    for paper in papers:
        # Find the submission number
        sub_num = None
        for reader in paper.content['authors']['readers']:
            if "Submission" in reader:
                sub_num = int(reader.split("Submission")[1].split("/")[0])
        if sub_num is None:
            raise ValueError(f"Could not find submission number for paper ID {paper.id}")

        # Download the paper PDF
        paper_id = paper.id
        with open(f"{out_dir}/{sub_num:03d}.pdf", "wb") as f:
            f.write(client.get_pdf(id=paper_id))

if __name__ == "__main__":
    main()
