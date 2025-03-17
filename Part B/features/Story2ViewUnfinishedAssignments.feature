Feature: Filter Unfinished Assignments
    As a student
    I want to view unfinished assignments
    So that I can keep track of unfinished work

    Background: API is running
        Given the API is running

    Scenario Outline: View unfinished assignments (Normal Flow)
        Given the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | false      |
        | A2    | Assignment 2 | true       |
        | A3    | Assignment 3 | false      |
        When a student views unfinished assignments
        Then the unfinished assignments are displayed

        Examples:
            | title | description |
            | A1    | Assignment 1 |
            | A3    | Assignment 3 |
    

    Scenario: View unfinished assignments with no unfinished assignments (Alternate Flow)
        Given the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | true       |
        | A2    | Assignment 2 | true       |
        | A3    | Assignment 3 | true       |
        When a student views unfinished assignments
        Then no unfinished assignments are displayed


#Expected Behavior: The system should return an error message when the doneStatus is not a boolean value (400 Bad Request)
#Actual Behavior: The system does not return an error message when the doneStatus is not a boolean value (200 OK)
    Scenario: View unfinished assignments with invalid doneStatus (Error Flow)
        Given the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | false      |
        | A2    | Assignment 2 | false      |
        | A3    | Assignment 3 | false      |
        When a student views unfinished assignments with invalid doneStatus "maybe"
        Then no unfinished assignments are displayed