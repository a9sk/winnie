import requests
import time
import json

modified_address = ""
search_payload = {}
api_key = ""
version = ""

def initial_setup():

    url = input("[?] Insert the url: ")

    if not url.startswith("http://") and not url.startswith("https://"):
        print("[!] Invalid URL format, Use an URL starting with 'http://' or 'https://'")
        exit
    
    global version
    version = input("[?] Insert the version: ")
    if not version:
        print("[!] The version is required")
        exit

    global modified_address
    modified_address = generate_address(url)

    global api_key
    api_key = input("[?] Insert your API key (see the documentation to get it): ")

    if not api_key:
        print("[!] API key is required")
        exit

    num_fields = int(input("[?] Enter the number of fields: "))

    filter_payload = {}
    for i in range(num_fields):
        field = input(f"[?] Enter field {i+1}: ")
        value = input(f"[?] Enter value for {field}: ")
        filter_payload[field] = value

    global search_payload
    search_payload = {
        "api_key": api_key,
        "filter": filter_payload
    }

def generate_address(url):

    parts = url.split('.')
    mod_address = f"{parts[0]}-apl.{parts[1]}/api/v{version}"
    return mod_address

def make_post_request(url, payload):

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def write_logs(logs, filename):

    with open(filename, 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        for log in logs:
            file.write(f"--------{timestamp}--------:\n {json.dumps(log)}\n")

def main():

    search_url = f"{modified_address}/events/search"

    search_response = make_post_request(search_url, search_payload)

    search_id = search_response.get("search_id")

    if search_id:

        show_payload = {
            "api_key": api_key,
            "search_id": search_id,
            "page": 1
        }

        show_url = f"{modified_address}/events/show"
        
        show_response = make_post_request(show_url, show_payload)

        events = show_response.get("events")

        write_logs(events, "events_logs.json")
    else:
        print("[!] No search_id was found in the response")


if __name__ == "__main__":

    initial_setup()

    while True:
        main()
        time.sleep(600)