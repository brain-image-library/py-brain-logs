import re
from datetime import datetime

import pandas as pd


def __get_failure_rate(df):
    """
    Retrieve the failure rate of an access file.
    Failure rate is defined as (number of 200 status code & is a bot) / (number of bot requests)
    """

    # Is the request from a bot?
    is_bot = df["is_bot"]

    # Is the request a success and from a bot?
    is_success_and_bot = (df["status_code"] == "200") & is_bot

    return len(df[is_success_and_bot]) / len(df[is_bot])


methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"]
pattern = r'^([\d.]+) - - \[([^]]+)\] "([^"]*)" (\d+) (\d+) "([^"]*)" "([^"]*)" "-"$'

with open("data/access.log", "r") as file:
    data = []
    lines = file.readlines()

    for line in lines:
        matches = re.match(pattern, line)
        if matches:
            ip_address = matches.group(1)
            timestamp = matches.group(2)
            request_line = matches.group(3)
            status_code = matches.group(4)
            size = matches.group(5)
            referrer = matches.group(6)
            user_agent = matches.group(7)

            split_request = request_line.split(" ")

            method = split_request[0] if split_request[0] in methods else ""
            url = split_request[1] if split_request[0] in methods else split_request[0]

            dataset = {
                "ip": ip_address,
                "date": datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z"),
                "method": method,
                "url": url,
                "status_code": status_code,
                "size": size,
                "referrer": referrer,
                "user_agent": user_agent,
                "is_bot": "bot" in user_agent.lower(),
            }

            data.append(dataset)
        else:
            print("No match found.")

df = pd.DataFrame(data)
