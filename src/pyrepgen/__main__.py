import logging
import argparse
from pathlib import Path

import os
import sys
import yaml

from .gitlab_fetch import fetch_all_commits

def main() -> None:

    parser = argparse.ArgumentParser(
        prog="pyrepgen",
        description="Generate reports from GitLab/GitHub repositories for verification reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="TODO"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        metavar="FILE",
        help="YAML configuration file path"
    )
    
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]: %(message)s",
    )
    
    logging.info("Starting report generation")
    
    # Load YAML config
    config_path = args.config
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    
    gitlab_url   = data.get("gitlab_url", "")
    project_id   = data.get("project_id", "")
    ref_name     = data.get("ref_name", "main")
    output_json  = data.get("output_json", "commits.json")

    logging.info("Getting information from GitLab API")
    logging.info(f"GitLab URL: {gitlab_url}")
    logging.info(f"Project ID: {project_id}")
    logging.info(f"Branch: {ref_name}")

    access_token = os.environ.get("GITLAB_TOKEN")
    if not access_token:
        logging.error("GITLAB_TOKEN environment variable not set")
        sys.exit(1)
        
    all_commits = fetch_all_commits(
        gitlab_url=gitlab_url,
        project_id=project_id,
        access_token=access_token,
        ref_name=ref_name,
        output_json=output_json
    )
    

    # all_commits = fetch_all_commits(
    #     gitlab_url=GITLAB_URL,
    #     project_id=PROJECT_ID,
    #     access_token=GITLAB_TOKEN,
    # )

    # commit_dates = group_commits_by_data(all_commits)
    # all_dates, all_counts = get_freqs(commit_dates)

    # logging.info(f"Total commits fetched: {len(all_commits)}")


if __name__ == "__main__":
    main()
