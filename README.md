# Graph-Theory-Project

This document is divided into seven sections
1. [Introduction](#s1)
2. [Understanding the problem](#s2)
3. [Understanding Neo4J](#s3)
4. [Finding a solution](#s4)
5. [Building the prototype](#s5)
6. [Using the system](#s6)
7. [Conclusion](#s7)

### <a id="s1"></a>Introduction
This is my 3rd year graph theory project. For this project I was required to design a database for a timetabling system for a third level institute. The database stores data about student groups, classrooms, lecturers, work hours and other data relating to timetables. This is the design document for the project. Note that this project also comes with a prototype database and a data folder. The data folder contains python scripts and data files that were used to format data and populate the prototype database. These are used later in the document.

### <a id="s2"></a>Understanding the problem
The timetabling problem, in its simplest form, is trying to allocate shared resources to a given timeslot. These resources include lecturers, rooms and student groups. These resources are limited and must be scheduled in such a way that they are uniquely allocated per timeslot, meaning a lecturer can only teach one class at a time, a student group can only attend one class at a time and a room can only be used for a single class at a time. The more resources that must be scheduled the more difficult this problem gets.

#### Resource constraints
This problem gets more difficult when considering the constraints on each resource.

+ Lecturers have work hours which means they can teach a limited amount of classes per week.
+ Rooms have a capacity meaning student groups should be assigned to appropriately sized rooms.
+ Some classes may require extra equipment which will also determine what room they will be allocated.
+ Student groups and lecturers need breaks between a certain number of classes.

All these factors make it very difficult to find a solution to the timetabling problem.

### <a id="s3"></a>Understanding Neo4J
Before trying to solve the timetabling problem it is important to first understand Neo4J and how it works.

#### What is Neo4J?
[Neo4J](https://neo4j.com/) is a graph database management system. Graph databases are catagorised as NoSQL, or not only SQL, databases. Unlike relational databases, NoSQL databases do not follow a set schema. This allows the data to be more flexible. Graph databases are particularly useful for storing connections, or relationships, between data.

#### How does Neo4J store data?
All data in a Neo4J database is represented as one of the following five structures:

1. Nodes
	
	A node in Neo4J is similar to a record in a relational database.
2. Labels
	
	Nodes can have labels. Labels are used to associate a set of nodes. Nodes with the same label are grouped together. In a relational database labels would be equivalent to tables.
3. Relationships
	
	Relationships are what connect the nodes in the graph. Neo4J is a multi-directional graph meaning the relationships, or edges, have direction. However, this direction can be ignored in queries. There can also be more than one relationship between any two nodes. Relationships can be compared to joins in relational databases, but because they are predefined it is much faster.
4. Relationship types
	
	Relationship types are used to describe how two nodes are related to each other. This is usually a verb. Relationship types are mandatory in Neo4J.
5. Properties
	
	Properties are key-value pairs that store data in nodes and relationships. As mentioned before, Neo4J is schemaless, therefore each node or relationship can have different properties even if they have the same labels or relationship types. Properties are similar to columns in relational databases.

### <a id="s4"></a>Finding a solution

#### What functionality is required?
Before developing a solution, its important to define what functionality this system should offer. The following is a list of proposed features for such a system.

+ Show the timetable for a course.
+ Show the timetable for a lecturer.
+ Show the current working hours for a lecturer.
+ Show the timetable for a room.
+ Show appropriate sized rooms available at a given time.

These features must be considered when modeling this problem with Neo4J.

#### What data needs to be stored?
Analysing both the problem, and the current GMIT timetabling system, helped determine what data this system needs to store. A brief break down is given below.

+ College
    
    The college using this timetabling system.
+ Campus

    The college may have different campuses.
+ Rooms
	
	Rooms will be identified by room numbers. Every room has a capacity and a type, such as lecture room, computer room and so on. Each room is within a campus.
+ Department 
    
    Each campus is divided into one or more departments.
+ Course

    Each department can run several courses. Courses are identified by an id and name.
+ Modules
    
    Each course has several modules. Modules are also identified by an id and name. More than one lecturer can teach a single module. Also, many courses can share the same module. Modules also change depending on the semester.
+ Year groups
	
	Year groups are identified by a unique code and are divided into student groups.
+ Student groups
	
	Student groups are identified by a combination of the year group and a group name, for example, group A, B and C. Each student group will have a different size that must be accounted for. However, it is not necessary to store all students as separate nodes.
+ Lecturers
	
	Lecturers are identified by their staff Id and name. Their maximum working hours should be stored. Each lecturer works for a department in a campus.
+ Classes
	
	Classes are identified by a combination of the time and day for which it is scheduled. Classes will also have a duration, type which will correspond with the type of classroom is required, a lecturer and will also belong to a module.
	
#### Researching solutions
Before trying to solve this problem I researched solutions and techniques proposed by others to solve this problem. Graph Colouring seemed to be a very common approach when dealing with the timetabling problem. It can be divided into vertex and edge colouring.

1. Vertex colouring
	It is a way of colouring the vertices of a graph such that no two adjacent vertices share the same colour.

2. Edge colouring
	It is a way of colouring the edges of a graph such that no two adjacent edges share the same colour.

"Colouring" a vertex or edge simply means giving it a label. Many algorithms exist to colour a graph with the minimum amount of colours. This is called the chromatic number. In relation to the timetabling problem, vertex colouring can be used to create a graph like the following.

![An example of a coloured graph](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/3-coloringEx.svg/160px-3-coloringEx.svg.png)

In this graph the vertices could represent classes. The edges could represent conflicts between classes. For example, if two classes share the same room, student group or lecturer. The colours could represent the timeslot in which that particular class is scheduled for. When constructing the timetable graph we know that in order to avoid a conflict we must not connect two nodes of the same colour. The maximum amount of colours the graph can have in this case is equal to the number of timeslots available in a week.

Other areas of interest were Tabu Search and Genetic Algorithm. However, these were not applicable when working with Neo4J.

#### Using graph theory to model this problem
Before starting the design it's important to be aware of the type of data thats being handled and how this system will be used. Generally, timetabling systems are updated seldom, usually one major write is made at the beginning of each semester and some minor adjustments might be made throughout the semester. However, the data will be read frequently so queries that read data must be efficient. Also, the queries that will be run on the data must be kept in mind. The first solution that came to mind was to design the graph as follows.

![Graph design - simple solution](https://g.gravizo.com/svg?digraph%20G%20%7B%3B%0ASTUDENT_GROUP%20%5Blabel%3D%22STUDENT_GROUP%5Cnnumber_of_students%3A%2025%22%5D%3B%0ALECTURER%20%5Blabel%3D%22LECTURER%5Cnid%3A%20%27G00123456%27%2C%5Cnname%3A%20%27John%20Smith%27%2C%5Cnmax_work_hours%3A%2038%22%5D%3B%0AROOM%20%5Blabel%3D%22ROOM%5Cnname%3A%20%27944%27%2C%5Cncapacity%3A%2090%22%5D%3B%0ACLASS%20%5Blabel%3D%22CLASS%5Cnday%3A%201%2C%5Cnstart%3A%2010%2C%5Cnend%3A%2012%2C%5Cntype%3A%20%27Practical%27%2C%5Cnmodule%3A%20%27Graph%20Theory%27%22%5D%3B%20%3B%0ASTUDENT_GROUP%20-%3E%20CLASS%20%5Blabel%3D%22ATTENDS%22%5D%3B%0ALECTURER%20-%3E%20CLASS%20%20%5Blabel%3D%22TEACHES%22%5D%3B%0AROOM%20-%3E%20CLASS%20%20%5Blabel%3D%22HOSTS%22%5D%3B%0A%7D%2529%3B)

In this solution the direction would be used to indicate a resource that is ALLOCATED TO a class. This design was influenced by the graph colouring solution. The simplicity of this approach would offer a lot of flexibility, for example, it doesn't restrict more than one lecturer from teaching the same module. This design would also make querying student, lecturer and room timetables very easy as only adjacent Class nodes will make up their timetable as those are the only classes they are allocated to. However, this design is flawed as it ignores a lot of data which needs to be stored such as courses and departments. Although this solution was not used, it was a good starting point thst helped clarify the relationships between the data which ultimately aided in the design of the final solution.

Given the list of data given above that needs to be stored, it seems intuitive to make each bullet point a label in the graph and the data in the paragraphs properties of those nodes. Therefore, there would be ten labels which are COLLEGE, CAMPUS, ROOM, DEPARTMENT, COURSE, MODULE, YEAR_GROUP, STUDENT_GROUP, LECTURER and CLASS.

Then the problem emerges how to connect or relate these nodes to each other. This is less straight forward. When designing the graph I started with the college node and worked down to the class nodes. However, after some trial and error I began to rethink this design and eventually came up with the solution shown in the following diagram.

![Graph design - final solution](https://g.gravizo.com/svg?digraph%20G%20%7B%0ACOLLEGE%20%5Blabel%3D%22COLLEGE%5Cnname%3A%20%27GMIT%27%22%5D%3B%0ACAMPUS%20%5Blabel%3D%22CAMPUS%5Cnname%3A%20%27Galway%27%22%5D%3B%0ADEPARTMENT%20%5Blabel%3D%22DEPARTMENT%5Cnname%3A%20%27Computer%20Science%5Cnand%20Applied%20Physics%27%22%5D%3B%0AROOM%20%5Blabel%3D%22ROOM%5Cnnumber%3A%20944%2C%5Cncapacity%3A%2090%22%5D%3B%0ACOURSE%20%5Blabel%3D%22COURSE%5Cntitle%3A%20%27Computing%20in%5CnSoftware%20Development%27%2C%5Cncourse_code%3A%20%27KSOFG%27%5Cnlevel%3A%207%22%5D%3B%0AYEAR_GROUP%20%5Blabel%3D%22YEAR_GROUP%5Cnyear_code%3A%2073%2C%5Cnyear%3A%203%22%5D%0ALECTURER%20%5Blabel%3D%22LECTURER%5Cnid%3A%20%27G00123456%2C%27%5Cnname%3A%20%27John%20Smith%27%2C%5Cnwork_hours%3A%2038%22%5D%3B%0AMODULE%20%5Blabel%3D%22MODULE%5Cnname%3A%20%27Software%20Testing%27%2C%5Cncourse_code%3A%2041879%2C%5Cnsemester%3A%202%22%5D%3B%0ACLASS%20%5Blabel%3D%22CLASS%5Cnday%3A%201%2C%5Cnstart%3A%2010%2C%5Cnend%3A%2012%2C%5Cntype%3A%20%27Practical%27%2C%5Cngroup%3A%20%27C%27%22%5D%3B%20%0ACOLLEGE%20-%3E%20CAMPUS%20%5Blabel%3D%22HAS%22%5D%3B%0ACAMPUS%20-%3E%20DEPARTMENT%20%20%5Blabel%3D%22HAS%22%5D%3B%0ACAMPUS%20-%3E%20ROOM%20%20%5Blabel%3D%22HAS%22%5D%3B%0ADEPARTMENT%20-%3E%20COURSE%20%20%5Blabel%3D%22RUNS%22%5D%3B%0ADEPARTMENT%20-%3E%20LECTURER%20%5Blabel%3D%22EMPLOYS%22%5D%3B%0ACOURSE%20-%3E%20YEAR_GROUP%20%5Blabel%3D%22ENROLLS%22%5D%3B%0AYEAR_GROUP%20-%3E%20MODULE%20%5Blabel%3D%22STUDIES%22%5D%3B%0AMODULE%20-%3E%20CLASS%20%5Blabel%3D%22SUBJECT_OF%22%5D%3B%0ALECTURER%20-%3E%20MODULE%20%5Blabel%3D%22TEACHES%22%5D%3B%0AROOM%20-%3E%20CLASS%20%5Blabel%3D%22HOSTS%22%5D%3B%0A%7D)

This design would utilise all of the data structures offered by Neo4J. It is designed to be flexible and to reduce duplicate and redundant data. A few of the design decisions made included:

+ Making the student group a property of a class node rather than a node itself as it would make querying timetables more difficult.
+ Creating a relationship between the lecturers and modules rather than the classes to avoid redundant relationships.
+ The semester property in the module node refers to the current semester for the college year, not the semester for the year group as this can be deduced from the year and semester properties.
+ The days on which the classes are sheduled are stored as numbers, where 1 represents Monday and so on.
+ The times for which the classes are sheduled are stored as numbers in a 24 hour format.

This is still a relatively simple design but it stores all the crucial data while remaining easy to understand.

### <a id="s5"></a>Building the prototype
Now that the database design is complete a prototype database can be built to demonstrate how it might be used. Note that this database will be stored at `/var/lib/neo4j/data/graph.db` in Linux.

#### Obtaining the data
To populate the prototype database, data is needed. Finding and extracting this data was more difficult than anticipated due to the implementation of GMIT's current timetabling system from which most of the data was extracted. In order to properly test this database design I tried to accumulate as much data as possible. However, this is only test data. It is not 100% complete and may contain minor errors.

##### Rooms
To get a list of rooms go to the [GMIT timetable website](http://timetable.gmit.ie/) and them choose Academic year 16/17, Rooms and then right click and choose the View Source option. The list of rooms will be available in the following format.

```
<option value="0484">G0484 CR1 (20)</option>
```

The data for each room is within a pair of opening and closing option tags. The first series of characters are a campus identifier and room number combination. The second set of data is the room name. At the end, within the round brackets, is the rooms capacity. After copying the list of rooms to a file I opened it with the Brackets editor which has a replace function that takes a regular expression. Using this feature I was able to remove the HTML option tags with the regular expression `<[^>]*>`. Once the file was in this format I used a Python script to parse it and write the data to a CSV file. This script takes a file called `rooms.txt` as an input and outputs a file called `rooms.csv` which can be loaded into Neo4J.

To run this script go to the `data/rooms` folder in a terminal and run `python room-parser.py`. Example files are provided.

##### Departments
To get a list of departments, again go to the [GMIT timetable website](http://timetable.gmit.ie/), Academic year 16/17, Programmes, right click and choose the View Source option. The list of rooms will be available in the following format.

```
<option value="9F6C92789472CF950AD128E4B39661ED">Galway Campus - Centre for the Creative Arts and Media</option>
```

The data for each room is again within a pair of opening and closing option tags. Because the list of departments is a small dataset there would be little benefit to writing a python script to parse it into the correct format. Instead I edited the in brackets with the help of regular expressions to produce a list in the following format.

```
"Galway","Dept of Computer Science & Applied Physics"
```

An example `departments.csv` file is provided in the `data` folder.

##### Courses
A list of courses is also available on the same page as the departments. This list will be available in the following format.

```
<option value="GA_KSOFT_7GM36SOF7">G-KSOFG73 BSc in Computing in Software Development L7 Yr 3 Sem 6</option>
```

Converting this list to a CSV file isn't as straight forward as there is no link between the department and course. Instead I selected each department on the [GMIT timetable website](http://timetable.gmit.ie/) and viewed each page source individually. I then copied them to different files called `dept-n.txt` and used the Brackets editor to remove the option tags and `&amp;` codes from the files. Then, using a python script I was able to combine these files into a single `courses.csv` file, using the department name from the `departments.csv` file created earlier. This file can then be loaded into Neo4J. To run this script go to the `data/courses` using a terminal and run `python course-parser.py`. Example files are provided.

##### Other data
Unfortunately, all the other data was too difficult to automatically obtain due to inconsistencies such as room and module names. Instead I manually created small datasets for the lecturers, modules and classes from data obtained from both the timetabling website and [LearnOnline](https://learnonline.gmit.ie/). I transformed this data into CSV format using the Brackets editor with the help regular expressions. This data relates only to the BSc in Computing in Software Development L7 course. These files are all within the `data` folder.

#### Adding the data to the database
Once the data is obtained we can start storing it in the prototype database. This section will involve importing the CSV files created earlier into the Neo4J database. If you are using Linux you must copy these CSV files into a folder found at `/usr/share/neo4j/import` to be able to import them into the database. Note that running the following queries will create a replica of the database provided in this repository.

The first node that needs to be created is the college node. The following query will create a single college node with a single property called name with the value 'GMIT'.

```
CREATE (c:College {name: "GMIT"});
```

Next create the room and campus nodes from the `rooms.csv` file created earlier, as shown below. This query first loads the `rooms.csv` file from the `import` folder. This file is read line by line, using the alias `line` to reference the current line of data. To retrieve data from the CSV file use the alias `line` and the column header, separated by a period. For each line we use the `MERGE` keyword to create a room node, with the name and capacity specified in the current line of the CSV file, if it does not already exist. We do the same for the campus nodes and the relationship between the campus and the room nodes.

```
LOAD CSV WITH HEADERS FROM "file:///rooms.csv" AS line
MERGE (r:Room { name: line.name, capacity: TOINT(line.capacity) })
MERGE (c:Campus { name: line.campus })
MERGE (c)-[:HAS]->(r);
```

Then, to create relationships between the college and campus nodes, use the `MATCH` keyword to find the college node that was created in the first query and all the campus nodes. Using `CREATE` we can then create a relationship between the college node and all the campus nodes.

```
MATCH (col:College {name: "GMIT"}), (c:Campus)
CREATE (col)-[:HAS]->(c);
```

Next, we'll create the department nodes and the relationships between the new departments and the campus nodes to which they belong. This data will be loaded from the `departments.csv` file, similar as to how the room data was loaded. Again, using the `MERGE` keyword, create the department and campus nodes if they do not already exist. Then create a relationship between them.

```
LOAD CSV WITH HEADERS FROM "file:///departments.csv" AS line
MERGE (d:Department { name: line.name })
MERGE (c:Campus { name: line.campus })
MERGE (c)-[:HAS]->(d);
```

Using a similar query to the one above we can create all course and year group nodes. This is a slightly longer query as the `courses.csv` contains a lot of different data. First, `USING` the match keyword, find the department node with a name value that matches the department column in the line of data. Next, using `MERGE`, check if a course node with the given course code exists. If not, create it. Then set the properties title and level. It's important to set these after using merge and not in it as some courses might have the same course code but a different title or level, which would lead to duplicate courses. Next, create a year group node. Finally, create a relationship between the department and course and course and year group nodes.

```
LOAD CSV WITH HEADERS FROM "file:///courses.csv" AS line
MATCH (d:Department { name: line.department })
MERGE (c:Course { course_code: line.course_code })
SET c.title = line.title
SET c.level = TOINT(line.level)
MERGE (d)-[:RUNS]->(c)
MERGE (c)-[:ENROLLS]->(y:Year_Group { year_code: line.year_code })
SET y.year = TOINT(line.year);
```

Next create the lecturers for the Computer Science and Applied Physics department, using the data from the `lecturers.csv` file, as shown below.

```
LOAD CSV WITH HEADERS FROM "file:///lecturers.csv" AS line
CREATE (l:Lecturer { id: line.id, name: line.name, work_hours: TOINT(line.work_hours) })
MERGE (d:Department { name: line.department })
MERGE (d)-[:EMPLOYS]->(l);
```

Create modules for the BSc in Computing in Software Development course, using the data from the `modules.csv` file. This file contains an array of lecturer names which will have to be handled. To do this, first use substring to remove the square brackets. Next, split the array using a comma as a delimiter. Then, use the `UNWIND` keyword to separate the array into multiple rows of data. Next, use `MATCH` to find the course using the `course_code` property and from that find the 3rd year node. Create the new module node and a relation between the year group and it. Finally, create a `TEACHES` relationship between the lecturer and module. Note that it is not a good idea to find the lecturer by name as more than one lecturer might have that name, however, staff Id's were not available when obtaining the data.

```
LOAD CSV WITH HEADERS FROM "file:///modules.csv" AS line
WITH line, split(substring(line.lecturers, 1, length(line.lecturers) -2), ",") AS lecturers 
UNWIND lecturers AS lecturer_name
MATCH (c:Course { course_code: "KSOFG", level: 7 })-[r]->(y:Year_Group { year: 3 })
MERGE (m:Module { module_code: line.module_code, name: line.name, semester: TOINT(line.semester) })
MERGE (y)-[:STUDIES]->(m)
MERGE (l:Lecturer { name: lecturer_name })
MERGE (l)-[:TEACHES]->(m);
```

Finally, create the class nodes from the data in the `classes.csv` file. Create relationships between the new class node and the lecturer, module and room nodes.

```
LOAD CSV WITH HEADERS FROM "file:///classes.csv" AS line
MATCH (r:Room { name: line.room })
MATCH (m:Module { name: line.module_name })
CREATE (cl:Class { day: TOINT(line.day), start: TOINT(line.start), end: TOINT(line.end), group: line.group_name, type: line.type })
MERGE (m)-[:SUBJECT_OF]->(cl)
MERGE (r)-[:HOSTS]->(cl);
```

Use the following query to view the entire graph. The first line increases the limit of nodes that are returned from the default 300 to 1000.

```
:config initialNodeDisplay:1000
MATCH (n)-[r]->(m) RETURN n, r, m;
```

### <a id="s6"></a>Using the system
Now that the prototype database contains all the test data we can use the following queries to retrieve useful data from it. This section will not include how to create data as that was covered in the previous section. Instead it will focus on the retrieval of data.

##### Room timetable
Find a room by name and return all the classes that are scheduled to be held in that room and the module which the class is for. Only return the classes that are run in the second semester of the year. The following query will return the timetable for the room with the name "0436 CR5".

```
MATCH (room:Room { name: "0436 CR5" })-[hosts:HOSTS]->(class:Class)
MATCH (module:Module { semester: 2 })-[subject_of:SUBJECT_OF]->(class:Class)
RETURN room, class, module
ORDER BY class.day, class.start;
```

Another important feature of a timetabling system was being able to display available rooms. The following query will find all room nodes with a capacity of at least 20 that are connected to a campus node with the name "Galway". If the room is connected to one or more class nodes ensure the room is only returned if it is not occupied at the given day and time, which in this case is Wednesday from 10 to 11. This query will only check classes that are on during the second semester of the year. Becasue rooms are a limited resource it's import to return the rooms that are a best fit. To achieve this, return the rooms in order of capacity.

```
MATCH (campus:Campus { name: "Galway" })-[r]->(room:Room)
WHERE room.capacity >= 20
OPTIONAL MATCH (room)-[r1:HOSTS]->(class:Class)<-[r2:SUBJECT_OF]-(module:Module { semester: 2 })
WITH room, COLLECT(class) AS classes
WHERE ALL(class IN classes
WHERE class.day <> 3 OR
(10 < class.start AND 11 <= class.start) 
OR (11 > class.end AND 10 >= class.end))
RETURN DISTINCT room
ORDER BY room.capacity;
```

This will return all rooms except room 0938 as there is a graph theory lecture on in that room at the given day and time.

##### Year group timetable
Get the year group by first finding a course by course code and then get the year group by entering the year. Return the year, the class and modules the year studies and the rooms in which the classes take place. Only return the timetable for the second semester of the year. For example, the following query will retrieve the 3rd year BSc in Computing in Software Development L7 timetable.

```
MATCH (course:Course { course_code: "KSOFG" })-[r1:ENROLLS]->(year:Year_Group { year: 3 })
MATCH (year)-[studies:STUDIES]->(module:Module { semester: 2 })
MATCH (module)-[subject_of:SUBJECT_OF]->(class:Class)
MATCH (room:Room)-[hosts:HOSTS]->(class:Class)
RETURN year, module, class, room
ORDER BY class.day, class.start;
```

##### Lecturer timetable
Find a lecturer by name and return all the classes they teach, the module to which that class is for and the room it is in. Only return the timetable for the second semester of the year. Order the results by day and time. The following query will return the timetable for the lecturer Ian McLoughlin. As mentioned earlier, using a staff Id would be more suitable for this query as two lecturers could share the same name, but staff Id's not available.

```
MATCH (lecturer:Lecturer { name: "Ian McLoughlin" })-[teaches:TEACHES]->(module:Module { semester: 2 })
MATCH (module)-[subject_of:SUBJECT_OF]->(class:Class)
MATCH (room:Room)-[hosts:HOSTS]->(class)
RETURN lecturer, module, class
ORDER BY class.day, class.start;
```

To get the lecturers weekly working hours we can use a similar query and change the return statement as shown below.

```
MATCH (lecturer:Lecturer { name: "Ian McLoughlin" })-[teaches:TEACHES]->(module:Module { semester: 2 })
MATCH (module)-[subject_of:SUBJECT_OF]->(class:Class)
MATCH (room:Room)-[hosts:HOSTS]->(class)
RETURN SUM(class.end - class.start) AS working_hours;
```

### <a id="s7"></a>Conclusion
The timetabling problem proved to be a very difficult problem to find an efficient solution to due to the high level of constraints and connectivity within the data and its non-linear nature. After completing this project I now see why graph theory is a suitable candidate for modeling such a problem.

This project provided an opportunity to learn more about Neo4J and graph databases in general. It allowed me to experiment with different techniques for designing a graph database, creating data in Neo4J and writing cypher queries. I now realise how important it is to choose an appropriate data structure when deciding how to store data. I found the Neo4J web interface very useful for visualising the data when testing queries.

If I was to do this project again I would like to research more about design patterns for graph databases and how to optimise a Neo4J database to improve performance especially when working with larger datasets.

References:
+ [Neo4J](https://neo4j.com/)
+ [Graph colouring on Wikipedia](https://en.wikipedia.org/wiki/Graph_coloring)
+ [Cypher cheat sheet](http://semanticommunity.info/@api/deki/files/25765/Neo4j_CheatSheet_v3.pdf)
+ [Importing CSV files with Cypher](https://neo4j.com/docs/developer-manual/current/get-started/cypher/importing-csv-files-with-cypher/)
+ [Importing CSV files containing array](https://dzone.com/articles/neo4j-load-csv-processing)
+ [GMIT timetable website](http://timetable.gmit.ie/)
+ [Gravizo was used to draw graphs](https://g.gravizo.com/)