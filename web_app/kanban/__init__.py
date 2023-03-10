import os

from flask import Flask
from flask import render_template


def create_app(test_config=None):

    #creates a Flask instance
    #__name__ (of the current module) to let the program know where it is in order to set up paths correctly 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', #change when deploying
        DATABASE=os.path.join(app.instance_path, 'kanban.sqlite'),
    )

    if test_config is None:
        # load config if not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load testing config
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #import db.py
    from . import db
    db.init_app(app)

    #import auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    #import task.py
    from . import task
    app.register_blueprint(task.bp)
    app.add_url_rule('/', endpoint='index')

    #landing page
    @app.route('/kanban')
    def kanban():
        return render_template("kanban.html") 

    return app

app = create_app()