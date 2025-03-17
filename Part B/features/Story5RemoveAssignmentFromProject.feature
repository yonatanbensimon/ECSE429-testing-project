Feature: Remove an Assignment from a Course
    As a student
    I want to remove an assignment from a course
    so that I can update my progress

    Background:
        Given the API is running and the student has the following assignments:
        | title | description | doneStatus |
        | A1    | Assignment 1 | true      |
        | A2    | Assignment 2 | false     |
        | A3    | Assignment 3 | true      |
        | A4    | Assignment 4 | false     |
        And the student has the following courses:
        | title | description | completed | active |
        | C1    | Course 1    | false     | true   |
        And the student has the following assignments in course C1:
        | title | description | doneStatus |
        | A1    | Assignment 1 | true      |
        | A2    | Assignment 2 | false     |
        | A3    | Assignment 3 | true      |
        | A4    | Assignment 4 | false     |

    Scenario Outline: Remove an unfinished assignment from a course (Normal Flow)
        When a student removes assignment "<assignment_title>" from course "<course_title>"
        Then assignment "<assignment_title>" is removed from course "<course_title>"

        Examples:
            | assignment_title | course_title |
            | A2               | C1           |
            | A4               | C1           |
            | A3               | C1           |
            | A1               | C1           |

    Scenario Outline: Remove an unfinished assignment from a course after completing it (Alternate Flow)
        When a student completes assignment <assignment_title>
        And a student removes assignment "<assignment_title>" from course "<course_title>"
        Then assignment "<assignment_title>" is removed from course "<course_title>" 

        Examples:
            | assignment_title | course_title |
            | A2               | C1           |
            | A4               | C1           |

    Scenario Outline: Remove an assignment from a course that doesn't exist (Error Flow)
        Given an assignment task with id <non-existent-id> does not exist 
        When a student removes assignment task with id <non-existent-id> from course C1
        Then an error message <message> is returned with status code <status_code>
    
        Examples:
            | non-existent-id | doneStatus | message | status_code |
            | 32    | true | Invalid GUID for 32 entity todo |  404 |
            | 33    | false | Invalid GUID for 33 entity todo | 404 |
            | 34    | false | Invalid GUID for 34 entity todo | 404 |
            | 35    | false | Invalid GUID for 35 entity todo | 404 |