from app import db
from app.models import Subject


class SubjectConf:

    @staticmethod
    def get_subjects_list():
        subjects_list = []
        for subject in Subject.query.all():
            subjects_list.append({
                'title': subject.title,
                'description': subject.description,
                'students': tuple({'name': teacher.full_name, 'id': teacher.id} for teacher in subject.teachers),
                'subjects': tuple({'name': student.full_name, 'id': student.id} for student in subject.students)
            })
        return subjects_list