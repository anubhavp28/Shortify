from app import sqldb

class Urls(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    url = sqldb.Column(sqldb.String(500), nullable=False)
    created_at = sqldb.Column(sqldb.TIMESTAMP, nullable=False)
    shorturl = sqldb.Column(sqldb.String(50), nullable=False)