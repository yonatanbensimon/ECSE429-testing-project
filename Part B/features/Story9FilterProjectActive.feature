Feature: Filter a project by active status
	As a student
	I want to be able to filter my course projects based on their active status
	So that I can easily focus on my ongoing courses
	
	Background: API is running, two false course projects exist, two true course projects exists
		Given the API is running
		And the following projects exists
		| p_id     | active |
		| ECSE 200 | true   |
		| ECSE 201 | false  |
		| ECSE 205 | true   |
		| ECSE 210 | false  |
	
	Scenario Outline: Get all projects with active status "true" (Normal Flow)
		When a student gets all project with an active status of "true"
		Then the response contains all <p_id>s with an active status of true
		And the response status is 200
		
		Examples:
		| p_id     |
		| ECSE 200 |
		| ECSE 205 |
	
	Scenario Outline: Get all projects with active status "true" when no active projects exists (Alternate Flow)
		Given there are no projects with "active" set to "true"
		When a students gets all course project with an active status of "true"
		Then the response status is 200
		And the response contains an empty list
	
	Scenario Outline: Get all projects with an invalid active status "<active>" (Error Flow)
		When a student gets all projects with invalid active status "<active>"
		Then the response status is 400
		And "<message>" is returned
		
		Examples:
		| p_id     | active | message                                     |
		| ECSE 200 | fals   | Failed Validation: active should be BOOLEAN |
