from models import User
from jira import JIRA

def push_to_jira(resp, content):
    jira = JIRA(resp.jira_server, basic_auth=(resp.jira_username, resp.jira_password))
    for issue in content:
        issue_dict = {
            "project": {"key": resp.jira_project_key},
            'summary': issue["title"],
            'description': issue["description"] + "\n\n" + "".join(f"-[ ] {i}\n" for i in issue["subtasks"]),
            # 'priority': {'name': issue["priority"]},
            'labels': [i.strip().replace(" ", "_").replace("-", "_") for i in issue["labels"]],
            "issuetype": {"id": "10005"}
        }
        issue = jira.create_issue(fields=issue_dict)
        print(f'Issue created successfully. Key: {issue.key}')