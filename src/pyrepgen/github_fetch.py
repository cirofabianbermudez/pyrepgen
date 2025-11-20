import logging
import requests
import json
from datetime import datetime, timedelta

def fetch_all_commits_github(config: dict, access_token: str) -> list:

    # Set up headers and initial parameters
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    page = 1
    per_page = 100
    all_commits = []

    # Prepare log file
    log_file = open(config["output_json"], "w", encoding="utf-8")
    log_file.write("[\n")
    first_entry = True

    url = f"{config["github_url"]}/repos/{config["owner"]}/{config["repo"]}/commits"

    while True:
        params = {
            "per_page": per_page,
            "page": page,
            "sha": config["sha"],
            "since": config["since"],
            "until": config["until"],
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            commits = response.json()
            
            if not commits:
                break
            
            for commit in commits:
                all_commits.append(commit)
                if not first_entry:
                    log_file.write(",\n")
                json.dump(commit, log_file, indent=2, ensure_ascii=False)
                first_entry = False

            logging.info(f"Fetched page {page}: {len(all_commits)} commits")
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching commits: {e}")
            break
        
    log_file.write("\n]")
    logging.info(f"JSON log saved to {config["output_json"]}")
    log_file.close()
    return all_commits
