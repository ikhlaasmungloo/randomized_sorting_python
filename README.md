This project is the first version of my senior design project where my group was supposed to build a web app that assigns senior design students 
into projects/teams based on their preferences. My role was to build the algorithm that would assign students into projects. 

Ideally, every students would get their first preference. However, all the students need to be equally distributed among the projects. In our case,
each project would have a maximum of 7 students(that number could not be hardcoded since the number of students and projects will change every year).Therefore, 
not all the students would get their first choice, but we still had to give them the best avaiable choice.

We were given 2 excel files where one of them contained the ids for each students and on of them contained all thier preferences for each project.
I had to merged the files and use the merged file to compute the algorithm. To be able to merge the original files provided to us and use them in my code, 
I had to clean them in excel and fix the column names. The cleaned up files can be viewed in my repository. 

For the first version of this project, I decided to select random students and assign them to groups based on their best available choice. For example, 
if thier first choice was some project X and project X was full/contained 7 students, I would move on to their second choice and so on until I found a project
that was not full and assigned them to that project. An output excel file was created to show all the all the projects and the students that were assigned into them.
I then created a plot using matplotlib to show how many students got each possible choice from 1-22. 

A lot of this process was done using Pandas. The code I wrote can be viewed in my repository as randomized_sorting.py. 

