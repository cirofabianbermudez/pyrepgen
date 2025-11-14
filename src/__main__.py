import logging
import requests
import json
from urllib.parse import quote

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def fetch_all_commits(gitlab_url: str, project_id: str, access_token: str) -> list:
    """
    Fetch all commits from a GitLab project using pagination.

    Returns:
        list: List of commit dictionaries.
    """

    # Set up headers and initial parameters
    headers = {
        "PRIVATE-TOKEN": access_token
    }
    page = 1
    per_page = 100
    all_commits = []
    commits_per_author = {}

    # Prepare log file
    log_filename = "commits.json"
    log_file = open(log_filename, "w", encoding="utf-8")
    log_file.write("[\n")
    first_entry = True
    
    encoded_id = quote(project_id, safe='')
    url = f"{gitlab_url}/api/v4/projects/{encoded_id}/repository/commits"

    while True:
        params = {
            "per_page": per_page,
            "page": page,
            "ref_name": "main",
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            commits = response.json()
            
            if not commits:
                break
            
            for commit in commits:
                # Skip merge commits, they have multiple parents
                parent_ids = commit.get('parent_ids', [])
                if len(parent_ids) > 1:
                    continue

                # author_email = commit.get("author_email") or "unknown"
                # commits_per_author[author_email] = commits_per_author.get(author_email, 0) + 1

                all_commits.append(commit)
                if not first_entry:
                    log_file.write(",\n")
                json.dump(commit, log_file, indent=2, ensure_ascii=False)
                first_entry = False

            # all_commits.extend(commits)
            logging.info(f"Fetched page {page}: {len(commits)} commits")
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching commits: {e}")
            break
        
    log_file.write("\n]")
    log_file.close()
    # print(commits_per_author)
    return all_commits

def group_commits_by_data(commits: list) -> dict:
    """
    """
    dates_freq = {}
    
    for commit in commits:
        committed_date = commit.get('committed_date', '')
        date = committed_date.split('T')[0]
        dates_freq[date] = dates_freq.get(date, 0) + 1
    
    return dates_freq

def get_freqs(dates_freq: dict) -> tuple[list, list]:
    """
    """

    date_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates_freq.keys()]
    start = min(date_objs)
    end = max(date_objs)

    all_dates = []
    all_counts = []

    current = start
    while current <= end:
        d_str = current.strftime("%Y-%m-%d")
        all_dates.append(current)               # keep as date; matplotlib handles it
        all_counts.append(dates_freq.get(d_str, 0))
        current += timedelta(days=1)

    return all_dates, all_counts


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]: %(message)s",
    )

    # Configurations
    GITLAB_URL   = "https://baltig.infn.it"
    PROJECT_ID   = "vip/gpio_uvc"
    GITLAB_TOKEN = ""

    logging.info("Getting information from GitLab API")
    logging.info(f"GitLab URL: {GITLAB_URL}")
    logging.info(f"Project ID: {PROJECT_ID}")
    
    all_commits = fetch_all_commits(
        gitlab_url=GITLAB_URL,
        project_id=PROJECT_ID,
        access_token=GITLAB_TOKEN,
    )

    commit_dates = group_commits_by_data(all_commits)
    all_dates, all_counts = get_freqs(commit_dates)
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(all_dates, all_counts, color="#7282ee")
    ax.fill_between(all_dates, all_counts, 0, alpha=0.3, color="#7282ee")
    ax.set_ylabel("Number of commits")
    ax.set_ylabel("Number of commits")

    # ax.xaxis.set_major_locator(mdates.MonthLocator())      # tick each month
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


    # Set y-axis limits
    ax.set_ylim(0, max(all_counts) + 1)

    # Set x-axis limits
    # Automatic
    # ax.set_xlim(all_dates[0], all_dates[-1])
    # Manual
    start = datetime(2024, 9, 1)
    end   = datetime(2024, 10, 24)
    
    # print(all_dates)
    ax.set_xlim(start, end)

    # Rotate x labels
    # for label in ax.get_xticklabels():
    #     label.set_rotation(90)

    # Grid
    ax.grid(True, axis="y", linestyle="-", alpha=0.5)

    plt.show()

    logging.info(f"Total commits fetched: {len(all_commits)}")
        
if __name__ == "__main__":
    main()
