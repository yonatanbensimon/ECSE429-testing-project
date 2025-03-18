Feature: Create a new project
	As a student
	I want to create a course project
	So that I can keep track of my different classes
	
	Background: API is running
		 Given the API server is running

	Scenario Outline: Create a course project (Normal Flow)
		When a student creates a course project with title "<title>" and description "<description>"
		Then the course project with title "<title>" and description "<description>" is created
		And the response status is 201
		
		Examples:
			| title    | description                | 
			| ECSE 200 | Electric Circuits 1 Course |
			| ECSE 210 | Electric Circuits 2 Course |
			| ECSE 222 | Digital Logic Course       |

	Scenario Outline: Create a course project that is currently inactive (Alternate Flow)
		When a student creates a course project for the upcoming semester with title "<title>" and active "false"
		Then the course project with title "<title>" and active "false" is created
		And the response status is 201

		Examples:
			| title    | active |
                        | ECSE 200 | false  |
                        | ECSE 210 | false  |
                        | ECSE 222 | false  |
	
	Scenario Outline: Create a course project with a non-boolean completed status (Error Flow)
		When a student creates a course project with an invalid completed status "<completed>"
		Then the response status is 400
		And "<message>" is returned

		Examples:
			| completed | message                                        |
			| hi        | Failed Validation: completed should be BOOLEAN |


