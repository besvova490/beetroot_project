import sys
from app import create_app, db, wb
from app.email import send_email
from app.models import Task, User
from config import basedir
from rq import get_current_job
from openpyxl.writer.excel import save_virtual_workbook

app = create_app()
app.app_context().push()
base_dir = basedir


def export_posts(user_id):
    job = get_current_job()
    task = Task.query.get(job.get_id())
    user_data = User.query.get(user_id).to_dict()
    try:
        ws = wb.active
        ws.append(['Lesson date', 'Status', 'Subject', 'Users',
                   'Phone number', 'Email'])
        for schedule in user_data['lesson_date']:
            users = tuple(user for user in schedule['users'] if user['is_teacher'] != user_data['is_teacher'])
            ws.append([schedule['time'], schedule['status'],
                      schedule['subject'], users[0]['full_name'],
                       users[0]['phone_number'], users[0]['email']
                       ])
        send_email('Scheduling form Beetroot Besvova490 PJ',
                   sender=app.config['MAIL_USERNAME'],
                   recipients=[user_data['email']],
                   text_body='This is scheduling your form '
                             'Beetroot Besvova490 PJ',
                   attachments=[("scheduling.xlsx", "application/vnd.ms-excel",
                                 save_virtual_workbook(wb))], sync=True)
        task.complete = True
        db.session.commit()
    except:
        task.complete = True
        db.session.commit()
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
