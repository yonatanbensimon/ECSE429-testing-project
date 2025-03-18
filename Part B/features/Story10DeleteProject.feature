Feature: Delete a project
	As a student
	I want to delete a course project
	So that I can clean up old courses
	
	Background: API is running
		Given the API is running
		And these projects exists:
		| p_id  | title |
		| 10    | test  |
		| 20    | test2 |
		| 30    | test3 | 
		| 40    | test4 |
	
	Scenario Outline: Delete a course project (Normal Flow)
		When a student deletes a course project with project id "<p_id>"
		Then the course project with id "<p_id>" is deleted
		And the response status is 404
		And when a students attempts to access the project with id "<p_id>" the response status is 404
		
		Examples:
		| p_id  |
		| 10    |
		| 30    |
		| 40    |

	Scenario Outline: Delete a course project with a title (Alternate Flow)
		When a student deletes a course project with title "<title>" and project id "<p_id>" 
		Then the course project with id "<p_id>" is deleted
             	And the response status is 404
                And when a students attempts to access the project with id "<p_id>" the response status is 404

		Examples:
                | p_id  |
                | 20    |
                | 30    |
                | 40    |

	Scenario Outline: Delete a course project with a non-existing project id
		When a student deletes a non-existent course project with project id "<p_id>"
		Then the response status is 404
		And "<message>" is returned
		
		Examples:
		| p_id  | message                                       |
		| 50    | Could not find any instances with projects/50 |
