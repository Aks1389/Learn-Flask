from flask import Flask
import redis
from rq import Queue

app2 = Flask(__name__)
r = redis.Redis()
q = Queue(connection=r)

from app2 import views
from app2 import tasks
