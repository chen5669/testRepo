from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_content():
    return dict(app=app, db=db, User=User, Role=Role)

# manager.add_command("shell",Shell(make_context=make_shell_content()))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
