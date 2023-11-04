import requests


def get_deals(auth_header: str):
  body = {"status": "success"}
  return requests.post("https://api.hubapi.com/crm/v3/objects/deals/search",
                       json=body,
                       headers=auth_header).json()


def get_tickets(auth_header: str):
  body = {"status": "success"}
  return requests.post("https://api.hubapi.com/crm/v3/objects/tickets/search",
                       json=body,
                       headers=auth_header).json()


def get_assosciated_tickets(deal_id, auth_header):
  body = {"inputs": [{"id": deal_id}]}
  data = requests.post(
    "https://api.hubapi.com/crm/v3/associations/Deals/Tickets/batch/read",
    headers=auth_header,
    json=body).json()["results"][0]["to"]
  ticket_ids = [x["id"] for x in data]
  return ticket_ids


def get_total_data(api_key: str):
  auth_header = {"Authorization": f"Bearer {api_key}"}
  result = {"result": []}
  all_deals = get_deals(auth_header)["results"]
  all_tickers = get_tickets(auth_header)["results"]
  for deal in all_deals:
    tickets = []
    assosciated_tickets = get_assosciated_tickets(deal["id"], auth_header)
    for ticket in all_tickers:
      if (ticket["id"] in assosciated_tickets and ticket["archived"] is False):
        tickets.append(ticket)

    ans = {"deal": deal, "associated_tickets": tickets}
    result["result"].append(ans)
  return result