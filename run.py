from app import app, db
from app.models import User, Subject, Scheduling


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subject': Subject, 'Scheduling': Scheduling}


if __name__ == '__main__':
    app.run(debug=True)
