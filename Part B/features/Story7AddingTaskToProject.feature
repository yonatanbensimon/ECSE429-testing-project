Feature: Add a Task to a project
	As a student
	I want to add an assignment task to one of my course project
	So that I can keep track of the different assignments due for my task

	Background: API is running, projects are created
		Given the API is running
		And a project with ID "<p_id>" exists
		And a task with ID "<t_id>" exists

	Scenario Outline: Add an assignment task to an existing project (Normal Flow)
		When a student adds an assignment task with id <t_id> to a project with id <p_id>
		Then the task with id <t_id> is added to the project with id <p_id>
		And the response status is 201

		Examples:
		| p_id | 
		| 1    | 

	Scenario Outline: Add an assignment task to a project where this task is already assigned to that project (Alternate Flow)
		Given that the task with "<t_id>" is already linked to the project with id "<p_id>"
		When a students adds the assignment task with id <t_id> to the project with id "<p_id>"
		Then the response status is 201
		
		Examples:
		| p_id | 
		| 1    | 

	Scenario Outline: Add an assignment task with a non existant id to an existing project (Error Flow)
		When a students adds an assignment task with a non existend id "<t_id>" to project with id "<p_id>"
		Then the response status is 404
		And "<message>" is returned
	
		Examples:
		| p_id | t_id | message                                    |
		| 2    | 5    | Could not find thing matching value for id |
