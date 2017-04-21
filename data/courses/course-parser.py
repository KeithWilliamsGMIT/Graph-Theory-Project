import csv
import re

# CSV file writter
out = csv.writer(open("courses.csv", "w"), delimiter=',',quoting=csv.QUOTE_ALL)

headerRow = ["department", "course_code", "title", "level", "year", "year_code", "semester", "group_name"]
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
        i = i + 1
        
        for module in modules:
            # Course Code and Year Code
            course_code = re.findall("^.*-(.+?)(?= )", module)[0]
            year_code = course_code[-2:]
            course_code = course_code[:-2]

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
            
            # Group (Default to A)
            group_stings = re.findall("^.*\sGr\s(\w)\s", module)
            group_name = "A"

            if len(group_stings) > 0:
                group_name = group_stings[len(group_stings) - 1]
                title = title.replace("Gr " + str(group_name), '')

            # Remove leading and trailing whitespaces
            title = title.strip()

            row = [department, course_code, title, level, year, year_code, semester, group_name]
            out.writerow(row)