Datamodeling and business logic of quiz rubric

Terminologies - Quiz is an assignment.
QuizSession is the object for user sub- mission of the assignment.
Rubrics is the collection of grading criteria for a single quiz.
This collection is in the form of a tree structure.
Every node in this collection is a single criteria having a name and maximum marks.


Load Data to DB -
python manage.py read_from_csv --read-file=<source_file_path>

Dump to CSV -
python manage.py dump_to_csv --dump-file==<destination_file_path>

Queries -

1. Given a name of rubric and quiz identifier, how many marks did student get.
=> python manage.py queries --query=1 <rubric-name> <quiz-id>
    returns list of students with total marks in given rubric and quiz

2. Given a name of rubric and quiz identifier, what is the average marks of the class.
=> python manage.py queries --query=1 <rubric-name> <quiz-id>
    returns average marks of class in given rubric and quiz

3. Given a quiz and a student identifier, what are the three rubrics student is really good at.
=> python manage.py queries --query=1 <quiz-id> <student-id>
    returns list of top 3 students with highest mark
