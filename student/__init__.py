'''
    Student App Project
    created by: Ajay
    created on: Feb 08, 2019

    - This file tell the python interpreter to consider this folder App(student) as python project.
    - This file is neccessary for configuring our app and  its database.
'''

import os

from flask import Flask

'''
    Factory functons for our Application will be used to register all modules and blueprints to app.
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'student.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    '''
        Basic route to check if the app and server are runnning, It will throw a Welcome message.
        To see the below code in browser set all flask variable and run server as:
        -> flask run
        -> Go to browser and type 127.0.0.1:5000/welcome
    '''
    @app.route('/welcome')
    def hello():
        return "<h2 align='center'> Welcome to Student App </h2>"


    '''
        Initializing the database for our application and registering in factory
    '''
    from . import student_db  # import from current directory to get register
    student_db.init_app(app)  # this will initialize the student_db with the app currently created here.

    '''
        Initializing the auth blueprint inside this factory method.
    '''
    from . import auth
    app.register_blueprint(auth.bp) # regiter the auth vlueprint to app.
    #app.add_url_rule('/', endpoint='index')


    from . import student
    app.register_blueprint(student.bp)
    #app.add_url_rule('/', endpoint='index')


    return app