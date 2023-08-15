import redis
import json
from flask import Flask, render_template

"""
    Nathan - 2724762
    FC Bayern - 557091
    TANZON - 2548827
    CB® BigSam - 1569017
    tuanmua - 2837821
    ALEXTUAN - 2728720
    Melencolia - 2547859
    loki - 1235112
    Linkvn - 2891330
    NhuomDoTroiAu - 2847489
"""

# app route
app = Flask(__name__)
@app.route('/')
def hello():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    user_list = json.loads(r.get('user_list').decode('utf-8'))
    vnt_list = json.loads(r.get('vnt_list').decode('utf-8'))
    result = r.get('result').decode('utf-8')
    return render_template('table.html', vnt_list=vnt_list, user_list=user_list, result=result)
