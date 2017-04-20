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
This is my 3rd year graph theory project. For this project I was required to design a database for a timetabling system for a third level institute. The database stores information about student groups, classrooms, lecturers and work hours.

### <a id="s2"></a>Understanding the problem
The timetabling problem, in its simplest form, is trying to allocate shared resources to a given timeslot. These resources include lecturers, rooms and student groups. These resources are limited and must be scheduled in such a way that they are uniquely allocated per timeslot, meaning a lecturer can only teach one class at a time, a student group can only attend one class at a time and a room can only be used for a single class at a time. The more resources that must be scheduled the more difficult this problem gets.

#### Resource constraints
This problem gets more difficult when considering the constraints on each resource.

+ Lecturers have work hours which means all the class they teach will have to be scheduled within those times.
+ Rooms have capacity meaning some student groups should be assigned to appropriately sized rooms.
+ Some classes may require extra equipment which will also determine what room they will be allocated.
+ Student groups and lecturers need breaks between a certain number of classes.

All these factors make it very difficult to find a solution to the timetabling problem.

### <a id="s3"></a>Understanding Neo4J
Before trying to solve the timetabling system problem it is important to first understand Neo4J and how it works.

#### What is Neo4J?
[Neo4J](https://neo4j.com/) is a graph database management system. Graph databases are catagorised as NoSQL, or not only SQL, databases. Unlike relational databases, NoSQL databases do not follow a set schema. This makes the data more flexible which allows for a more simple design. Graph databases are particularly useful for storing connections, or relationships, between data.

#### How does Neo4J store data?
All data is a Neo4J database is represented as one of the following five:

1. Nodes
	
	A node in Neo4J is similar to a record in a relational database.
2. Labels
	
	Nodes can have labels. Labels are used to associate a set of nodes. Nodes with the same label are grouped together. In a relational database labels would be equivalent to tables.
3. Relationships
	
	Relationships are what connect the nodes in the graph. Neo4J is a multi-directional graph meaning the relationships, or edges, have direction, but it can be ignored in queries, and there can be more than one relationship between any two nodes. Relationships can be compared to joins in relational databases, but because they are predefined it is much faster.
4. Relationship types
	
	Relationship types are used to describe how to nodes are related. This is usually a verb. Relationship types are mandatory in Neo4J.
5. Properties
	
	Properties are key-value pairs that store data in nodes and relationships. As mentioned before, Neo4J is schemaless, therefore each node or relationship can have different properties even if they have the same labels or relationship types. Properties are similar to columns in relational databases.

### <a id="s4"></a>Finding a solution

#### What functionality is required?
Before developing a solution, its important to define what functionality this system should offer. The following is a list of proposed functions for such a system.

+ CRUD operations for students group, lecturers and rooms.
+ Show available rooms at a given time.
+ Show timetable for student group.
+ Show timetable for lecturer.
+ Show timetable for room.
+ Show alternative times and rooms for a given class. The times must suit both the lecturers and student groups timetable and the room must have an adequate capacity and equipment.

These functions must be considered when modeling this problem with Neo4J.

#### What data needs to be stored?
Analysing both the problem, and the current GMIT timetabling system, helped determine what data this system needs to be stored. A brief break down is given below.

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
	
	Year groups will be identified by a unique code. Year groups are broken into Student groups.
+ Student groups
	
	Student groups will be identified by a combination of the year group and a group name, for example, group A, B and C. Each student group will have a different size that must be accounted for. However, it is not necessary to store all students as separate nodes.
+ Lecturers
	
	Lecturers will be identified by their staff ID and name, Their working hours should be stored. Each lecturer works for a department in a campus.
+ Classes
	
	Classes will have a will be identified by a combination of the time and day for which it is scheduled. Classes will also have a duration, type which will correspond with the type of classroom is required, a lecturer and will also belong to a module.
	
#### Researching other solutions
Before trying to solve this problem I researched solutions and techniques proposed by others to solve this problem. The following is what I found.

##### Graph Colouring
This seemed to be a very common approach when dealing with the timetabling problem. It can be divided into vertex and edge colouring.

1. Vertex colouring
	It is a way of colouring the vertices of a graph such that no two adjacent vertices share the same colour.

2. Edge colouring
	It is a way of colouring the edges of a graph such that no two adjacent edges share the same colour.

"Colouring" a vertex or edge simply means giving it a label. Many algorithms exist to colour a graph with the minimum amount of colours. This is called the chromatic number. In relation to the timetabling problem, vertex colouring can be used to create a graph like the following.

![An example of a coloured graph](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/3-coloringEx.svg/160px-3-coloringEx.svg.png)

In this graph the vertices could represent classes. The edges could represent conflicts between classes. For example, if two classes share the same room, student group or lecturer. The colours could represent the timeslot in which that particular class is scheduled for. When constructing the timetable graph we know that in order to avoid a conflict we must not connect two nodes of the same colour. The maximum amount of colours the graph can have in this case is equal to the number of timeslots available.

Sources: *[Wikipedia](https://en.wikipedia.org/wiki/Graph_coloring)*

#### Using graph theory to model this problem
Given the list of data given above that needs to be stored, it seems intuitive to make each bullet point a label in the graph and the data in the paragraphs properties of those nodes. Therefore there will be ten labels which are COLLEGE, CAMPUS, ROOM, DEPARTMENT, COURSE, MODULE, YEAR_GROUP, STUDENT_GROUP, LECTURER and CLASS.

Then the problem emerges how to connect or relate these nodes to each other. This is less straight forward. When designing the graph I started with the college node and worked down to the class nodes as shown in the following diagram.

![Graph design](https://g.gravizo.com/svg?digraph%20G%20%7B%0ACOLLEGE%20%5Blabel%3D%22COLLEGE%5Cnname%3A%20%27GMIT%27%22%5D%3B%0ACAMPUS%20%5Blabel%3D%22CAMPUS%5Cnname%3A%20%27Galway%27%22%5D%3B%0ADEPARTMENT%20%5Blabel%3D%22DEPARTMENT%5Cnname%3A%20%27Computer%20Science%5Cnand%20Applied%20Physics%27%22%5D%3B%0AROOM%20%5Blabel%3D%22ROOM%5Cnnumber%3A%20944%2C%5Cncapacity%3A%2090%2C%5Cntype%3A%20lecture%22%5D%3B%0ACOURSE%20%5Blabel%3D%22COURSE%5Cntitle%3A%20%27Computing%20in%5CnSoftware%20Development%27%2C%5Cncourse_code%3A%20%27KSOFG%27%5Cnlevel%3A%207%22%5D%3B%0AYEAR_GROUP%20%5Blabel%3D%22YEAR_GROUP%5Cnyear_code%3A%20%27B070306%27%2C%5Cnstart_year%3A%202014%22%5D%0ALECTURER%20%5Blabel%3D%22LECTURER%5Cnid%3A%20%27G00123456%2C%27%5Cnname%3A%20%27John%20Smith%27%2C%5Cnwork_hours%3A%2038%22%5D%3B%0ASTUDENT_GROUP%20%5Blabel%3D%22STUDENT_GROUP%5Cnname%3A%20%27C%27%5Cnnumber_of_students%3A%2025%22%5D%3B%0AMODULE%20%5Blabel%3D%22MODULE%5Cnname%3A%20%27Software%20Testing%27%22%5D%3B%0ACLASS%20%5Blabel%3D%22CLASS%5Cntime%3A%2010%2C%5Cnduration%3A%202%2C%5Cntype%3A%20%27Practical%27%22%5D%3B%20%0ACOLLEGE%20-%3E%20CAMPUS%20%5Blabel%3D%22HAS%22%5D%3B%0ACAMPUS%20-%3E%20DEPARTMENT%20%20%5Blabel%3D%22HAS%22%5D%3B%0ACAMPUS%20-%3E%20ROOM%20%20%5Blabel%3D%22HAS%22%5D%3B%0ADEPARTMENT%20-%3E%20COURSE%20%20%5Blabel%3D%22RUNS%22%5D%3B%0ADEPARTMENT%20-%3E%20LECTURER%20%5Blabel%3D%22EMPLOYS%22%5D%3B%0ACOURSE%20-%3E%20YEAR_GROUP%20%5Blabel%3D%22ENROLLS%22%5D%3B%0AYEAR_GROUP%20-%3E%20STUDENT_GROUP%20%5Blabel%3D%22HAS%22%5D%3B%0AYEAR_GROUP%20-%3E%20MODULE%20%5Blabel%3D%22STUDIES%5Cnsemester%3A%206%22%5D%3B%0AMODULE%20-%3E%20CLASS%20%5Blabel%3D%22SUBJECT%20OF%22%5D%3B%0ALECTURER%20-%3E%20CLASS%20%5Blabel%3D%22TEACHES%22%5D%3B%0AROOM%20-%3E%20CLASS%20%5Blabel%3D%22HOSTS%22%5D%3B%0ASTUDENT_GROUP%20-%3E%20CLASS%20%5Blabel%3D%22ATTENDS%22%5D%3B%0A%7D)

This design would utilise all of the data structures offered by Neo4J. This solution is designed to be flexible and to reduce duplication. This design would also making querying student, lecturer and room timetables very easy as only adjacent class nodes will be returned.

### <a id="s5"></a>Building the prototype
Now that the database design is complete a prototpye database can be built to demonstrate how it might be used.

#### Obtaining the data
To populate the prototpe database data is needed. Finding and extracting this data was more difficult than anticipated due to the implementation of GMIT's current timetabling system. 

##### Rooms
To get a list of rooms I went to the [GMIT timetable website](http://timetable.gmit.ie/). To get the list of rooms go to Academic year 16/17, Rooms and then right click and choose the View Source option. The list of rooms will be available in the following format.

```
<option value="0484">G0484 CR1 (20)</option>
```

The data for each room is within a pair of opening and closing option tags. The first series of characters are a campus identifier and room number combination. The second set of data is the room name. At the end, within the round brackets, is the rooms capacity. After copying the list of rooms to a file I opened it with the Brackets editor which has a replace function that takes a regular expression. Using this feature I was able to remove the HTML option tags with the regular expression `<[^>]*>`. Once the file was in this format I used a Python script to parse it and write the data to a CSV file. This script takes a file called `rooms.txt` as an input and outputs a file called `rooms.csv` which can be loaded into Neo4J.

To run this script go to the `data/rooms` in the terminal and type python `room-parser.py`. Example files are provided.

### <a id="s6"></a>Using the system

### <a id="s7"></a>Conclusion