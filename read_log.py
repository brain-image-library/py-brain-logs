import re
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt

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


def __get_date_count(df):
    # Create a frequency of days and requests (e.g. datetime.date(2022, 5, 16): 12337
    return df["date"].apply(lambda dt: dt.date()).value_counts().sort_index()


def __get_date_chart(df):
    """
    Create a chart that will showcase the amount of requests per day.
    """
    frequencies = __get_date_count(df)

    # Create the bar chart
    plt.bar(frequencies.index, frequencies.values)
    plt.xlabel("Date")
    plt.ylabel("Number of Requests")
    plt.title("Number of Requests per Day")
    plt.xticks(rotation=45)

    # Display the chart
    plt.margins(0.05)
    plt.tight_layout()
    plt.show()
