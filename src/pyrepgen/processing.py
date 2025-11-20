from datetime import datetime, timedelta

def normalize_gitlab_dommits():
    pass

def normalize_github_commits():
    pass


def filter_commits_by_author_email(commits: list, author_email: str) -> list:
    filter_commits = []
    for commit in commits:
        if commit.get("author_email") == author_email:
            filter_commits.append(commit)
            
    return filter_commits


def filter_out_merge_commits(commits: list) -> list:
    filter_commits = []
    for commit in commits:
        parent_ids = commit.get("parent_ids", [])
        if len(parent_ids) > 1:
            continue
        filter_commits.append(commit)

    return filter_commits


def build_commit_histogram_by_date(commits: list) -> dict:
    dates_freq = {}
    
    for commit in commits:
        committed_date = commit.get('committed_date', '')
        date = committed_date.split('T')[0]
        dates_freq[date] = dates_freq.get(date, 0) + 1
    
    return dates_freq


def fill_missing_days_in_histogram(dates_freq: dict) -> tuple[list, list]:
    date_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates_freq.keys()]
    start = min(date_objs) + timedelta(days=-1)
    end = max(date_objs) + timedelta(days=1)

    all_dates = []
    all_counts = []

    current = start
    while current <= end:
        d_str = current.strftime("%Y-%m-%d")
        all_dates.append(current)
        all_counts.append(dates_freq.get(d_str, 0))
        current += timedelta(days=1)

    return all_dates, all_counts