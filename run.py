from app import app, db
from app.models import Teacher, Student, Subject, Scheduling


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Teacher': Teacher,
            'Student': Student, 'Subject': Subject, 'Scheduling': Scheduling}


if __name__ == '__main__':
    app.run()
