from mongoengine import Document, StringField
from secret_keys import default_openai

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField()
    full_name = StringField()
    company_product_offering = StringField()
    hubspot = StringField()
    openai_key = StringField(
        required=True,
        default=default_openai
    )
    jira_server = StringField()
    jira_username = StringField()
    jira_password = StringField()
    jira_project_key = StringField()


