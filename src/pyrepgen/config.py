from pathlib import Path
import yaml

class ConfigError(Exception):
    pass

def load_config(config_path: Path, tool: str) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_path} does not exist")
    
    try:
        text = config_path.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
    except Exception as e:
        raise ConfigError(f"Failed to read or parse YAML: {e}")
    
    if tool == "gitlab": 
        gitlab_url = data.get("gitlab_url", "")
        project_id = data.get("project_id", "")
        if not gitlab_url or not project_id:
            raise ConfigError("gitlab_url and project_id must be specified in the YAML config file")
        data.setdefault("ref_name", "main")
        data.setdefault("output_json", "gitlab_commits.json")

    if tool == "github": 
        github_url = data.get("github_url", "")
        repo = data.get("repo", "")
        owner = data.get("owner", "")
        if not github_url or not repo or not owner:
            raise ConfigError("github_url, repo and owner must be specified in the YAML config file")
        data.setdefault("sha", "main")
        data.setdefault("output_json", "github_commits.json")

    # Default values for optional fields
    data.setdefault("author_email", "unknown@email.com")
    data.setdefault("author", "Unknown Author")
    data.setdefault("since", None)
    data.setdefault("until", None)

    # Default values for plotting parameters
    data.setdefault("x_lim_start", None)
    data.setdefault("x_lim_end", None)
    data.setdefault("y_lim_top", None)
    data.setdefault("y_lim_bottom", None)
    data.setdefault("marker_left", None)
    data.setdefault("marker_right", None)

    return data
