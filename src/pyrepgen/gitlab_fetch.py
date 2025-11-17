import logging
import requests
import json
from datetime import datetime, timedelta

def fetch_all_commits(gitlab_url: str, 
                      project_id: str, 
                      access_token: str,
                      ref_name: str,
                      output_json: str) -> list:
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
    log_filename = output_json
    log_file = open(log_filename, "w", encoding="utf-8")
    log_file.write("[\n")
    first_entry = True
    
    encoded_id = project_id.replace("/", "%2F")
    url = f"{gitlab_url}/api/v4/projects/{encoded_id}/repository/commits"

    while True:
        params = {
            "per_page": per_page,
            "page": page,
            "ref_name": ref_name,
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
            logging.info(f"Fetched page {page}: {len(all_commits)} commits")
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching commits: {e}")
            break
        
    log_file.write("\n]")
    log_file.close()
    return all_commits


def group_commits_by_data(commits: list) -> dict:
    """
    Returns:
        dict: Dictionary with dates as keys and number of commits as values.
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