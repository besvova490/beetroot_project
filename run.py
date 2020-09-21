from app import create_app, db, jwt
from app.models import User, Subject, Scheduling, Task

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subject': Subject,
            'Scheduling': Scheduling, 'Task': Task, 'jwt': jwt}


if __name__ == '__main__':
    app.run(debug=True)
