from app import db
from app.models import Student


class StudentConf:

    @staticmethod
    def students_list():
        student_list = []
        for student in Student.query.all():
            student_list.append({
                'name': student.full_name,
                'email': student.email,
                'students': tuple({'name': teacher.full_name, 'id': teacher.id} for teacher in student.teachers),
                'subjects': tuple({'name': subjects.title, 'id': subjects.id} for subjects in student.subjects)
            })
        return student_list
