import pandas as pd

from datetime import datetime

with open('data/access.log', 'r') as file:
    data = []
    for line in file.readlines():
        # Split the log entry based on spaces
        fields = line.split(' ')

        dataset = {
            'ip': fields[0],
            'date': datetime.strptime(fields[3].lstrip('[') + fields[4].strip(']'), '%d/%b/%Y:%H:%M:%S%z'),
            'method': fields[5].strip('').strip('"'),
            'url': fields[6],
            'status_code': fields[8],
            'size': fields[9]
        }

        data.append(dataset)


df = pd.DataFrame(data)
