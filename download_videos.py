"""Download all videos from OpenReview."""
import pathlib

import openreview
import getpass

VENUE = "NeurIPS.cc/2025/Workshop/AI4Music"

def main():
    """Download all videos from OpenReview."""
    # Make sure the output directory exists
    out_dir = pathlib.Path("videos")
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
        # Skip if video file is not present
        if "video_file" not in paper.content:
            continue

        # Find the submission number
        sub_num = None
        for reader in paper.content['authors']['readers']:
            if "Submission" in reader:
                sub_num = int(reader.split("Submission")[1].split("/")[0])
        if sub_num is None:
            raise ValueError(f"Could not find submission number for paper ID {paper.id}")

        # Download the video
        paper_id = paper.id
        with open(f"{out_dir}/{sub_num:03d}.mp4", "wb") as f:
            f.write(client.get_attachment(id=paper_id, field_name="video_file"))

if __name__ == "__main__":
    main()
