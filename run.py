from app import app, db
from app.models import User, Subject


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subject': Subject}


if __name__ == '__main__':
    app.run(debug=True)
