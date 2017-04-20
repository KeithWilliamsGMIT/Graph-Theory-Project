import csv
import re

with open("rooms.txt") as f:
    rooms = f.readlines()

# CSV file writter
out = csv.writer(open("rooms.csv", "w"), delimiter=',',quoting=csv.QUOTE_ALL)

row = [rooms, 1]
headerRow = ["campus", "name", "capacity"]
out.writerow(headerRow)

for room in rooms:
    # campus
    campus_id_length = 4
    
    if re.search('G', room[:1], re.IGNORECASE):
        campus = 'Galway'
        campus_id_length = 1
    elif re.search('MAYO', room[:campus_id_length], re.IGNORECASE):
        campus = 'Mayo'
    elif re.search('LETT', room[:campus_id_length], re.IGNORECASE):
        campus = 'Letterfrack'
    elif re.search('CCAM', room[:campus_id_length], re.IGNORECASE):
        campus = 'Centre for Creative Arts & Media'
    elif re.search('NUIG', room[:campus_id_length], re.IGNORECASE):
        campus = 'NUIG'
    else:
        campus = 'Unknown'
        campus_id_length = 0
    
    # Name
    name = room[campus_id_length:].rsplit(' (')[0]
    
    # Capacity - The last number is the capacity
    numbers = re.findall('\d+', room)
    capacity = numbers[len(numbers) - 1]
    
    row = [campus, name, capacity]
    out.writerow(row)