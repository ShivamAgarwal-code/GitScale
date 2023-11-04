import mongoengine
from models import User

mongoengine.connect("ProductCopilot")

User.objects.update(
    set__jira_server="https://keshav-garg.atlassian.net/",
    set__jira_username="keshavgarg8800@gmail.com",
    set__jira_password="ATATT3xFfGF0R3NprXIFobzrWdxIecJp8nmhOdsREA3TSchuTCMS6dFn6oRVcXTFJEzVBEXFQ6HGqIK_Z4ALqECzbpnK_tTpOLgGeGKBBp7nqnZWZhWquboKO-uz4KxQbeayxXKqJbDNGEXsmdYPd0RQMjAjjkCm5GEMG18KFwFIGx6h3P16DDY=4EA9A801",
    set__jira_project_key="HAC"
)