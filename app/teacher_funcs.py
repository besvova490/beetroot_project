from app import db
from app.models import Teacher


class TeacherConf:

    @staticmethod
    def teachers_list():
        teachers_list = []
        for teacher in Teacher.query.all():
            teachers_list.append({
                'name': teacher.full_name,
                'email': teacher.email,
                'students': tuple({'name': student.full_name, 'id': student.id} for student in teacher.students),
                'subjects': tuple({'name': subjects.title, 'id': subjects.id} for subjects in teacher.subjects)
            })
        return teachers_list
