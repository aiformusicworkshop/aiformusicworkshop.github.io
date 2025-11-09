"""Download all videos from OpenReview."""
import argparse
import json
import pathlib

import getpass
import openreview

VENUE = "NeurIPS.cc/2025/Workshop/AI4Music"

def parse_args():
    """Download all videos from OpenReview."""
    parser = argparse.ArgumentParser(description="Download all videos from OpenReview.")
    parser.add_argument("-o", "--out_dir", type=pathlib.Path, default="videos")
    return parser.parse_args()

def main():
    """Download all videos from OpenReview."""
    # Parse command-line arguments
    args = parse_args()

    # Make sure the output directory exists
    args.out_dir.mkdir(exist_ok=True)

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

    # Initialize a dictionary to store the output
    out_dict = {}

    # Iterate over all the papers
    for paper in papers:
        # Skip if no video link or file is present
        if "video_link" not in paper.content and "video_file" not in paper.content:
            continue

        # Find the submission number
        sub_num = None
        for reader in paper.content["authors"]["readers"]:
            if "Submission" in reader:
                sub_num = int(reader.split("Submission")[1].split("/")[0])
        if sub_num is None:
            raise ValueError(f"Could not find submission number for paper ID {paper.id}")

        # Check if a video link is present
        if "video_link" in paper.content:
            out_dict[sub_num] = paper.content["video_link"]["value"]
            continue

        # Download the video
        paper_id = paper.id
        with open(f"{args.out_dir}/{sub_num:03d}.mp4", "wb") as f:
            f.write(client.get_attachment(id=paper_id, field_name="video_file"))

    # Save the output dictionary to a JSON file
    out_dict = dict(sorted(out_dict.items()))
    with open(f"{args.out_dir}/video_links.json", "w", encoding="utf-8") as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
