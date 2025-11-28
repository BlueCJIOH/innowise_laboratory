PRAGMA foreign_keys = ON;

BEGIN;

DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  full_name TEXT NOT NULL,
  birth_year INTEGER NOT NULL CHECK (birth_year >= 1900)
);

CREATE TABLE grades (
  id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL,
  subject TEXT NOT NULL,
  grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
  FOREIGN KEY (student_id) REFERENCES students(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_grades_subject ON grades(subject);
CREATE INDEX idx_students_birth_year ON students(birth_year);

INSERT INTO students (full_name, birth_year) VALUES
  ('Alice Johnson', 2005),
  ('Brain Smith', 2004),
  ('Carla Reyes', 2006),
  ('Daniel Kim', 2005),
  ('Eva Thompson', 2003),
  ('Felix Nguyen', 2007),
  ('Grace Patel', 2005),
  ('Henry Lopez', 2004),
  ('Isabella Martinez', 2006);

WITH student_ids AS (
  SELECT id, full_name FROM students
)
INSERT INTO grades (student_id, subject, grade) VALUES
  ((SELECT id FROM student_ids WHERE full_name = 'Alice Johnson'), 'Math', 88),
  ((SELECT id FROM student_ids WHERE full_name = 'Alice Johnson'), 'English', 92),
  ((SELECT id FROM student_ids WHERE full_name = 'Alice Johnson'), 'Science', 85),
  ((SELECT id FROM student_ids WHERE full_name = 'Brain Smith'), 'Math', 77),
  ((SELECT id FROM student_ids WHERE full_name = 'Brain Smith'), 'History', 83),
  ((SELECT id FROM student_ids WHERE full_name = 'Brain Smith'), 'English', 87),
  ((SELECT id FROM student_ids WHERE full_name = 'Carla Reyes'), 'Science', 95),
  ((SELECT id FROM student_ids WHERE full_name = 'Carla Reyes'), 'English', 74),
  ((SELECT id FROM student_ids WHERE full_name = 'Carla Reyes'), 'Art', 89),
  ((SELECT id FROM student_ids WHERE full_name = 'Daniel Kim'), 'Math', 84),
  ((SELECT id FROM student_ids WHERE full_name = 'Daniel Kim'), 'Science', 88),
  ((SELECT id FROM student_ids WHERE full_name = 'Daniel Kim'), 'Physical Education', 93),
  ((SELECT id FROM student_ids WHERE full_name = 'Eva Thompson'), 'English', 90),
  ((SELECT id FROM student_ids WHERE full_name = 'Eva Thompson'), 'History', 85),
  ((SELECT id FROM student_ids WHERE full_name = 'Eva Thompson'), 'Math', 88),
  ((SELECT id FROM student_ids WHERE full_name = 'Felix Nguyen'), 'Science', 72),
  ((SELECT id FROM student_ids WHERE full_name = 'Felix Nguyen'), 'English', 81),
  ((SELECT id FROM student_ids WHERE full_name = 'Felix Nguyen'), 'Art', 94),
  ((SELECT id FROM student_ids WHERE full_name = 'Grace Patel'), 'Science', 77),
  ((SELECT id FROM student_ids WHERE full_name = 'Grace Patel'), 'Math', 90),
  ((SELECT id FROM student_ids WHERE full_name = 'Henry Lopez'), 'History', 77),
  ((SELECT id FROM student_ids WHERE full_name = 'Henry Lopez'), 'English', 78),
  ((SELECT id FROM student_ids WHERE full_name = 'Henry Lopez'), 'Science', 80),
  ((SELECT id FROM student_ids WHERE full_name = 'Isabella Martinez'), 'English', 96),
  ((SELECT id FROM student_ids WHERE full_name = 'Isabella Martinez'), 'Math', 99),
  ((SELECT id FROM student_ids WHERE full_name = 'Isabella Martinez'), 'Art', 92);

COMMIT;


-- find all grades for a specific student (Alice Johnson).
SELECT s.full_name, g.subject, g.grade
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson'
ORDER BY g.subject;


-- calculate the average grade per student.
SELECT s.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC, s.full_name;


-- list all students born after 2004.
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year, full_name;


-- list all subjects and their average grades.
SELECT subject, ROUND(AVG(grade), 2) AS avg_grade
FROM grades
GROUP BY subject
ORDER BY subject;


-- find the top 3 students with the highest average grades.
WITH student_avg AS (
  SELECT s.id, s.full_name, AVG(g.grade) AS avg_grade
  FROM students AS s
  JOIN grades AS g ON g.student_id = s.id
  GROUP BY s.id, s.full_name
)
SELECT full_name, ROUND(avg_grade, 2) AS avg_grade
FROM student_avg
ORDER BY avg_grade DESC, full_name
LIMIT 3;


-- show all students who have scored below 80 in any subject.
SELECT DISTINCT s.full_name, s.birth_year
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
WHERE g.grade < 80
ORDER BY s.full_name;
