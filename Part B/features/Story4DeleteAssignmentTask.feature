Feature: Deleting a completed assignment

    As a student
    I want to delete a completed assignment
    So that I can keep track of my assignments
    
    Background: API is running
        Given the API is running and the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | true      |
        | A2    | Assignment 2 | false     |
    
    Scenario Outline: Delete a completed assignment (Normal Flow)
        When a student deletes an assignment task with title <title>
        Then the assignment task with title <title> is deleted

        Examples:
            | title |
            | A1    |
            | A2    |

    Scenario Outline: Delete an incomplete assignment after completing it (Alternate Flow)
        When a student completes assignment <title>
        And a student deletes an assignment task with title <title>
        Then the assignment task with title <title> is deleted
        
        Examples:
            | title |
            | A1    |
            | A2    |
    
    Scenario Outline: Delete an assignment task which doesn't exist (Error Flow)
        Given an assignment task with id <non-existent-id> does not exist 
        When a student deletes assignment task with id <non-existent-id>
        Then an error message <message> is returned with status code <status_code>
    
        Examples:
            | non-existent-id | doneStatus | message | status_code |
            | 32    | true | Could not find any instances with todos/32 | 404 |
            | 33    | false | Could not find any instances with todos/33 | 404 |
            | 34    | false | Could not find any instances with todos/34 | 404 |