from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from datetime import datetime, timedelta
import random

fake = Faker()

# Підключення до бази даних
engine = create_engine('sqlite:///school.db')
Session = sessionmaker(bind=engine)
session = Session()

# Функція для генерації випадкового рейтингу
def generate_grades():
    return random.randint(60, 100)

# Створення груп
groups = [Group(name=f'Group {i+1}') for i in range(3)]
session.add_all(groups)
session.commit()

# Створення викладачів
teachers = [Teacher(name=fake.name()) for _ in range(3)]
session.add_all(teachers)
session.commit()

# Створення предметів
subjects = [Subject(name=f'Subject {i+1}', teacher=random.choice(teachers)) for i in range(5)]
session.add_all(subjects)
session.commit()

# Створення студентів та їх оцінок
for _ in range(30):
    student = Student(name=fake.name(), group=random.choice(groups))
    session.add(student)
    for subject in subjects:
        for _ in range(random.randint(3, 5)):
            grade_date = fake.date_time_between(start_date='-1y', end_date='now')
            grade = Grade(student=student, subject=subject, grade=generate_grades(), date=grade_date)
            session.add(grade)

session.commit()

print("Database seeding completed!")
