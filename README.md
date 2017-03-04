# Graph-Theory-Project
This is my 3rd year graph theory project. For this project I was required to design a database for a timetabling system for a third level institute. The database stores information about student groups, classrooms, lecturers and work hours.

### Understanding the problem
The timetabling problem, in its simplest form, is trying to allocate shared resources to a given timeslot. These resources include lecturers, rooms and student groups. These resources are limited and must be scheduled in such a way that they are uniquely allocated per timeslot, meaning a lecturer can only teach one class at a time, a student group can only attend one class at a time and a room can only be used for a single class at a time. The more resources that must be scheduled the more difficult this problem gets.

#### Resource constraints
This problem gets more difficult when considering the constraints on each resource.

+ Lecturers have work hours which means all the class they teach will have to be scheduled within those times.
+ Rooms have capacity meaning some student groups should be assigned to appropriately sized rooms.
+ Some classes may require extra equipment which will also determine what room they will be allocated.
+ Student groups and lecturers need breaks between a certain number of classes.

All these factors make it very difficulat to find a solution to the timetabling problem.

### Understanding Neo4J
Before trying to solve the timetabling system problem it is important to first understand Neo4J and how it works.

#### What is Neo4J?
[Neo4J](https://neo4j.com/) is a graph database management system. Graph databases are catagorised as NoSQL, or not only SQL, databases. Unlike relational databases, NoSQL databases do not follow a set schema. This makes the data more flexible which allows for a more simple design. Graph databases are particularly useful for storing connections, or relationships, between data.

#### How does Neo4J store data?
All data is a Neo4J database is represented as one of the following five:

1. Nodes
2. Relationships
3. Relationship types
4. Labels
5. Properties

### Finding a solution

#### What functionality is required?

#### Using graph theory to model this problem

### Obtaining the data

### Using the system

### Conclusion