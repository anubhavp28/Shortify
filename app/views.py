from app import app, redisdb, sqldb
from app.models import Urls
from app import errors
from flask import request, jsonify, redirect
from hashlib import md5
from base64 import urlsafe_b64encode
import time    

@app.route('/shorten', methods=['GET'])
def shorten():
    if not request.args.get('url'):
        return errors.bad_request("No or invalid URL provided.")
    url = request.args.get('url')

    def hash8(msg):
        return urlsafe_b64encode(md5(msg.encode()).digest())[:8]

    short_url = hash8(url).decode('ascii')
    redisdb.set(short_url, url)
    persistent_entry = Urls(url=url, shorturl=short_url, created_at=time.strftime('%Y-%m-%d %H:%M:%S'))
    sqldb.session.add(persistent_entry)
    sqldb.session.commit()
    return jsonify({ "status" : "success", "short_url" : short_url })

@app.route('/lookup/<short_url>', methods=['GET'])
def lookup(short_url):
    if not len(short_url) == 8:
        return errors.bad_request("No or invalid URL provided.")
    record = sqldb.session.query(Urls).filter_by(shorturl = short_url).first()
    if not record:
        return errors.notfound_404("This URL is not assigned to any link.")
    return jsonify({ "status" : "success", "link" : record.url, "created_at" : record.created_at, "short_url" : short_url})

@app.route('/go/<short_url>', methods=['GET'])
def go(short_url):
    if not len(short_url) == 8:
        return errors.bad_request("No or invalid URL provided.")
    link = redisdb.get(short_url) 
    if link:
        return redirect(link)
    return errors.notfound_404("This URL is not assigned to any link.")


    