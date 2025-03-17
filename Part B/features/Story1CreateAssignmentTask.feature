Feature: Creating an Assignment Task
    As a student
    I want to create an assignment task
    So that I can keep track of my assignments

    Background: API is running
        Given the API is running

    Scenario: Create an assignment task (Normal Flow)
        When a student creates an assignment task with title "A1" and description "Assignment 1"
        Then the assignment task with title "A1" and description "Assignment 1" is created

    Scenario: Create an assignment task without a description (Alternate Flow)
        When a student creates an assignment task with title "A1"
        Then the assignment task with title "A1" is created

    Scenario Outline: Create an assignment task without a title (Error Flow)
        When a student creates an assignment task with description "<description>"
        Then the assignment task with description "<description>" is not created and an error message "<message>" is returned
        
        Examples:
            | description | message |
            | Assignment 1 | title : field is mandatory |