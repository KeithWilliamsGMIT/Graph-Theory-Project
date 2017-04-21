import csv
import re

# CSV file writter
out = csv.writer(open("courses.csv", "w"), delimiter=',',quoting=csv.QUOTE_ALL)

headerRow = ["department", "course_code", "title", "level", "year", "semester"]
out.writerow(headerRow)
i = 1

with open('../departments.csv') as deptFile:
    reader = csv.DictReader(deptFile)
    for row in reader:
        # Department
        department = row['name']

        with open('dept-' + str(i) + ".txt") as courseFile:
            modules = courseFile.readlines()
        
        # Increment i so the next dept file is read on the next iteration
        ++i
        
        for module in modules:
            # Course Code
            course_code = re.findall("^.*-(.+?)(?= )", module)[0]

            # Title
            title = re.findall("(?= )(.*)", module)[0]

            # Level
            level_strings = re.findall("^.*\sL(\d)\s", module)
            level = ""

            if len(level_strings) > 0:
                level = level_strings[len(level_strings) - 1]
                title = title.split(" L" + str(level))[0]

            # Year
            year_stings = re.findall("^.*\sYr\s(\d)\s", module)
            year = ""

            if len(year_stings) > 0:
                year = year_stings[len(year_stings) - 1]
                title = title.split(" Yr " + str(year))[0]

            # Semester
            semester_stings = re.findall("^.*\sSem\s(\d)\s", module)
            semester = ""

            if len(semester_stings) > 0:
                semester = semester_stings[len(semester_stings) - 1]
                title = title.split(" Sem " + str(semester))[0]

            # Remove leading and trailing whitespaces
            title = title.strip()

            row = [department, course_code, title, level, year, semester]
            out.writerow(row)