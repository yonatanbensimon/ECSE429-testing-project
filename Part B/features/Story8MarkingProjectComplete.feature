Feature: Mark Project as completed
	As a student
	I want to mark a course project as completed
	So that I can keep track of the different classes I have succesfully completed
	
	Background: API is running, project exists
		Given the API server is running
		And a project with ID "<p_id>" exists
	
	Scenario Outline: Mark a class project as completed (Normal Flow)
		When a student modifies the completed status of project with id <p_id> with status "true"
		Then the completed status of the project with id "<p_id>" should be "false" 
		And the response status is 200
		
		Examples:
		| p_id |
		| 1    |
		| 2    |
	
	Scenario Outline: Mark a class project that is already completed as completed (Alternate Flow)
		Given that the class project with id <p_id> has a completed status of "true"
		When a student modifies the completed status of project with id <p_id> to "true"
		Then the response status is 200

		Examples:
		| p_id |
		| 3    |

	Scenario Outline: Mark a non existing class project as completed (Error Flow) 
		Given that the class project with id <p_id> does not exist
		When a student attempts to modify the completed status of project with id <p_id> to "true"
		Then the response status is 404
		And <message> is returned
		
		Examples
		| p_id | message                                                  |
		| 64   | No such project entity instance with GUID or ID 64 found |
