Feature: Creating an Assignment Task
    As a student
    I want to create an assignment task
    So that I can keep track of my assignments

    Background: API is running
        Given the API is running

    Scenario Outline: Create an assignment task (Normal Flow)
        When a student creates an assignment task with title "<title>" and description "<description>"
        Then the assignment task with title "<title>" and description "<description>" is created

        Examples:
            | title | description |
            | A1    | Assignment 1 |
            | A2    | Assignment 2 |
            | A3    | Assignment 3 |

    Scenario Outline: Create an assignment task without a description (Alternate Flow)
        When a student creates an assignment task with title "<title>"
        Then the assignment task with title "<title>" is created
        
        Examples:
            | title |
            | A1    |
            | A2    |
            | A3    |

    Scenario Outline: Create an assignment task without a title (Error Flow)
        When a student creates an assignment task with description "<description>"
        Then the assignment task with description "<description>" is not created and an error message "<message>" is returned
        
        Examples:
            | description | message |
            | Assignment 1 | title : field is mandatory |
            | Assignment 2 | title : field is mandatory |
            | Assignment 3 | title : field is mandatory |