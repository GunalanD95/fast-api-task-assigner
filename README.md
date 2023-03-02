# Title :  fastapi - ASSIGNMENT 

## GOAL 

```

There is a manual QC process which happens. 

There is a portal from which each individual qc task is assigned. 

The portal needs to check how many qc persons are logged in and which of the logged in persons are free, as in not on a task,

and automatically assign tasks. 

Once the task is finished the person will automatically get assigned the next task if any is pending.
 
How would you architect this? I want to understand step by step the methodology you used to come to the final solution. 
 
Can you illustrate a basic API framework written in Python using Flask and MySql as the database.

Do reply with a confirmation that you have received this email and 

let me know when you have completed the above challenges accordingly we will set up the next call.


```


## TODO
- Portal has Some Tasks and Persons
- Tasks should be assigned to only who is Logged in
- if there is no task , then we dont need to do anything
- if there is task in pipeline , then we need to assign to someone who is free 
- if no person is free task will stay in pipline

## INITIAL REQUIREMENTS

- Lets Create Task and Person Models