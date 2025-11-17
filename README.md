# pyrepgen

## Setup

```bash
export GITLAB_TOKEN="PUT YOUR PERSONAL ACCESS TOKEN HERE"
unset GITLAB_TOKEN

read -s -p "PUT YOUR PERSONAL ACCESS TOKEN HERE" GITLAB_TOKEN
echo
export GITLAB_TOKEN
```

```powershell
$env:GITLAB_TOKEN = "PUT YOUR PERSONAL ACCESS TOKEN HERE"
Remove-Item Env:GITLAB_TOKEN

$plain = Read-Host "PUT YOUR PERSONAL ACCESS TOKEN HERE"
$env:GITLAB_TOKEN = $plain
```

## References

[GitLab REST API - Commits API](https://docs.gitlab.com/api/commits/)