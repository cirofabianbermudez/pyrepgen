import logging
import argparse

import os
import sys
import yaml
import json


from .cli import build_parser
from .config import load_config, ConfigError

from .gitlab_fetch import fetch_all_commits_gitlab
from .github_fetch import fetch_all_commits_github

from .plot_manager import create_commit_plot
from .processing import (
    filter_out_merge_commits,
    filter_commits_by_author_email,
    build_commit_histogram_by_date,
    fill_missing_days_in_histogram,
)

def main() -> None:

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]: %(message)s",
    )
    
    # Parse command-line arguments
    parser = build_parser()
    args = parser.parse_args()

    # Log parsed arguments
    logging.info("=== CLI PARSER ===")
    logging.info(f"MODE:        {args.mode}")
    logging.info(f"TOOL:        {args.tool}")
    logging.info(f"YAML CONFIG: {args.config}")
    logging.info(f"INPUT JSON:  {args.input}")

    # Load configuration from YAML file
    try:
        config = load_config(args.config, args.tool)
    except ConfigError as e:
        logging.error(e)
        sys.exit(1)
        
    # Log configuration details
        logging.info(f"=== YAML configuration loaded ===")
    if args.tool == "gitlab":
        logging.info(f"GitLab URL:   {config["gitlab_url"]}")
        logging.info(f"Project ID:   {config["project_id"]}")
        logging.info(f"Branch:       {config["ref_name"]}")
        
    if args.tool == "github":
        logging.info(f"GitHub URL:   {config["github_url"]}")
        logging.info(f"Owner:        {config["owner"]}")
        logging.info(f"Repository:   {config["repo"]}")
        logging.info(f"SHA/Branch:   {config["sha"]}")

    logging.info(f"Output JSON:  {config["output_json"]}")
    logging.info(f"Author Email: {config["author_email"]}")
    logging.info(f"Since:        {config["since"]}")
    logging.info(f"Until:        {config["until"]}")

    if args.mode == "read":

        logging.info(f" === READ MODE ===")
        input_json = args.input

        # Read commits from input JSON file
        logging.info(f"Reading commits from: {input_json}")

        try:
            with open(input_json, "r", encoding="utf-8") as f:
                all_commits = json.load(f)
        except FileNotFoundError:
            logging.error(f"Input file {input_json} not found")
            sys.exit(1)

    else:

        logging.info(f" === NORMAL MODE ===")

        if args.tool == "gitlab":
            token_str = "GITLAB_TOKEN"
        if args.tool == "github":
            token_str = "GITHUB_TOKEN"
            
        access_token = os.environ.get(token_str)
        if not access_token:
            logging.error(f"{token_str} environment variable not set")
            sys.exit(1)
        logging.info(f"{token_str} found in environment variables")

        if args.tool == "gitlab":
            logging.info("Getting information from GitLab API")
            all_commits = fetch_all_commits_gitlab(config, access_token)
        if args.tool == "github":
            logging.info("Getting information from GitHub API")
            all_commits = fetch_all_commits_github(config, access_token)

    # Filter commits
    filter_commits = filter_out_merge_commits(all_commits)
    logging.info(f"Removing merge commits")
    logging.info(f"Extracted: {len(filter_commits)} commits")

    # filter_commits = filter_commits_by_author_email(filter_commits, author_email)
    # logging.info(f"Filtering by author email")
    # logging.info(f"Extracted: {len(filter_commits)} commits")

    # histogram = build_commit_histogram_by_date(filter_commits)
    # all_dates, all_counts = fill_missing_days_in_histogram(histogram)

    # logging.info(f"First commit date: {all_dates[0].strftime('%Y-%m-%d')}")
    # logging.info(f"Last commit date:  {all_dates[-1].strftime('%Y-%m-%d')}")

    # Generate plot
    # logging.info(f" === GENERATING COMMIT PLOT ===")
    # create_commit_plot(
    #     all_dates=all_dates,
    #     all_counts=all_counts,
    #     email=author_email,
    #     author=author,
    #     x_lim_start=x_lim_start,
    #     x_lim_end=x_lim_end,
    #     y_lim_top=y_lim_top,
    #     y_lim_bottom=y_lim_bottom,
    #     marker_left=marker_left,
    #     marker_right=marker_right,
    # )

if __name__ == "__main__":
    main()
