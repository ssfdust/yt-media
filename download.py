import requests
from app import app, db
from models import Person

import os.path as op
from PIL import Image

def create_thumb(src, dst):
    src_path = op.join('uploads', src)
    dst_path = op.join('uploads', dst)
    photo = Image.open(src_path)
    photo = photo.resize((100, 100), Image.ANTIALIAS)
    photo.save(dst_path)

def download_pic(url):
    resp = requests.get(url)
    filename = url[url.rfind("/") + 1:]
    filename_thumb = filename.replace(".", "_thumb.")
    src_path = op.join('uploads', filename)
    with open(src_path, 'wb') as src_fp:
        for block in resp.iter_content(1024):
            if not block:
                break
            src_fp.write(block)
    create_thumb(filename, filename_thumb)
    return filename

def download_person():
    url = 'http://api.public.ytcreativemedia.com//pc/renwu/all'
    resp = requests.get(url)
    json = resp.json()
    for item in json['list']:
        if item['cover']:
            pic = download_pic(item['cover'])
            item['cover'] = pic
    return json['list']

def load_to_person():
    person_info = download_person()
    for person in person_info:
        item = Person(name=person['subject_name'],
                      description=person['description'][:512],
                      thumbnail=person['cover'])
        db.session.add(item)
    db.session.commit()

def main():
    with app.app_context():
        load_to_person()


if __name__ == '__main__':
    main()
