import os
from app import create_app, db
from app.models import Employee, Role,Department
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_process():
    return {'db': db, 'employee': Employee, 'role': Role, 'department': Department}


if __name__ == "__main__":
    app.run()
