Feature: Update an Assignment task's status

    As a student
    I want to update an assignment task's status
    So that I can keep track of my progress
    
    Background: API is running
        Given the API is running and the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | false      |
        | A2    | Assignment 2 | true      |
    
    Scenario: Complete an assignment task (Normal Flow)
        When a student completes assignment A1
        Then the assignment task A1 is marked as complete
    
    Scenario: Uncomplete an assignment task (Alternate Flow)
        When a student uncompletes assignment A2
        Then the assignment task A2 is marked as incomplete   

    Scenario Outline: Update an assignment task which doesn't exist (Error Flow)
        Given an assignment task with id <non-existent-id> does not exist 
        When a student updates assignment task <non-existent-id> with status <doneStatus>
        Then an error message <message> is returned with status code <status_code>
    
        Examples:
            | non-existent-id | doneStatus | message | status_code |
            | 32    | true | Invalid GUID for 32 entity todo | 404 |