from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import Redis
import os

app = None
sqldb = None
redisdb = None

def create_app():
    global app, redisdb, sqldb
    app = Flask(__name__)
    
    def generate_config_from_env():
        return {
            "sql" : {
                "dbms" : os.environ['SHORTIFY_SQL_DBMS'],
                "host" : os.environ['SHORTIFY_SQL_HOST'],
                "port" : os.environ['SHORTIFY_SQL_PORT'],
                "username" : os.environ['SHORTIFY_SQL_USERNAME'],
                "password" : os.environ['SHORTIFY_SQL_PASSWORD'],
                "database" : os.environ['SHORTIFY_SQL_DATABASE']
            },
            "redis" : {
                "host" : os.environ['SHORTIFY_REDIS_HOST'],
                "port" : os.environ['SHORTIFY_REDIS_PORT'],
                "db" : os.environ['SHORTIFY_REDIS_DB'],
            }
        }
    
    config = generate_config_from_env()

    def configure_appinstance(app, config):
        sql = config['sql']
        redis = config['redis']
        app.config['SQLALCHEMY_DATABASE_URI'] = r'%s://%s:%s@%s:%s/%s' % (  sql['dbms'], 
                                                                            sql['username'],
                                                                            sql['password'],
                                                                            sql['host'],
                                                                            sql['port'],
                                                                            sql['database']
                                                                        )
        app.config['REDIS_HOST'] = redis['host']
        app.config['REDIS_PORT'] = redis['port']
        app.config['REDIS_DB'] = redis['db']
    
    configure_appinstance(app, config)
    sqldb = SQLAlchemy(app)
    redisdb = Redis(app)

    from app import models
    from app import views

    return app