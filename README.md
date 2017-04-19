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
+ Student groups
	
	Student groups will be identified by a group name, for example, group A, B and C. Each student group will have a different size that must be accounted for. However, it is not necessary to store all students as separate nodes.
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
Given the list of data given above that needs to be stored, it seems intuitive to make the bullet points nodes and labels in the graph and the data in the paragraphs properties of those nodes. Therefore there will be four labels which are Room, Group, Lecturer and Class.

Then the problem emerges how to connect or relate these nodes to each other. This is less straight forward. At first glance it seems that all nodes should be connected to a Class node. An example of these relationships might be as follows.

+ Room HOSTS Class
+ Group ATTENDS Class
+ Lecturer TEACHES Class

This design utilises all of the data structures offered by Neo4J except for relationship properties. In this solution the direction would be used to indicate a resource that is ALLOCATED TO a class. The simplicity of this approach would offer a lot of flexibility, for example, it doesn't restrict more than one lecturer from teaching the same module.

This design would also making querying student, lecturer and room timetables very easy as only adjacent Class nodes will make up their timetable as those are the only classes they are allocated to.

### <a id="s5"></a>Building the prototype

#### Obtaining the data


### <a id="s6"></a>Using the system

### <a id="s7"></a>Conclusion