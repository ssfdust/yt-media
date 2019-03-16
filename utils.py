from hashlib import md5
from uuid import uuid4
import os

def generate_md5(password):
    return md5(password.encode('utf-8')).hexdigest()

def gen_hash_filename(obj, file_data):
    _, ext = os.path.splitext(file_data.filename)
    random_name = uuid4().hex
    return '%s%s' % (random_name, ext)
