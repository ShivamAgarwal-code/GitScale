from models import User
from authentication import validate_user
from flask import make_response, jsonify
from hubspot import get_total_data
from open_ai import chat
from jira_connector import push_to_jira
import os


def process_hubspot_resp(raw_text):
    start_sent = "{}. Related to the {} deal which brings in the company ${} annually  cland the client is in the {} stage they have certain product requests:"
    k = 1
    proc_text_qn = []
    for i in raw_text["result"]:
        temp = start_sent.format(k, i["deal"]["properties"]["dealname"], i["deal"]["properties"]["amount"], i["deal"]["properties"]["dealstage"])
        for j in i["associated_tickets"]:
            temp += (j["properties"]["content"]+".")
            break
        if len(i["associated_tickets"]) != 0:
            proc_text_qn.append(temp)
            k += 1
    return "\n".join(proc_text_qn)


def proc_response(chat_response):
    print(chat_response)
    chat_response = chat_response.split("JIRA Task: ")[1:]
    print(chat_response)
    usefultags = []
    for i in chat_response:
        task = i.split("\n")
        temp = {
            "title": task[0],
            "description": task[1].split("Description: ")[-1],
            "subtasks": [i[4:] for i in task[3:6]],
            "labels": task[6].split("Labels: ")[-1].split(","),
            "priority": task[7].split("Priority: ")[-1]
        }
        usefultags.append(temp)
    return usefultags


def integrations_master(token, data):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    resp.update(__raw__={"$set":data})
    if data.get("hubspot", False):
        raw_crm_data = get_total_data(data["hubspot"])
        chatgpt_response = chat(resp.openai_key, resp.company_product_offering, process_hubspot_resp(raw_crm_data))
        # print(chatgpt_response)
        jira_contents = proc_response(chatgpt_response)
        push_to_jira(resp, jira_contents)
    return make_response(jsonify({"message": chatgpt_response}), 200)