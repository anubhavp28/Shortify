from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import Redis
import toml
import os.path

app = None
sqldb = None
redisdb = None

def create_app(pathtoconfig):
    if not os.path.isfile(pathtoconfig):
        raise ValueError('Non-existing file supplied for configuration.')

    with open(pathtoconfig, "r") as configfile:
        try:
            config = toml.load(configfile)
        except:
            #make it use default config file
            pass

    from pprint import pprint
    pprint(config)
    
    global app, redisdb, sqldb
    app = Flask(__name__)
    
    def configure_appinstance(app, config):
        sql = config['sqlbackend']
        redis = config['redis']
        app.config['SQLALCHEMY_DATABASE_URI'] = r'%s://%s:%s@%s:%d/%s' % (  sql['dbms'], 
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