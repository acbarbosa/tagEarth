# -*- coding: utf-8 -*-
from bottle import install, route, run, template, static_file, request
from landsat.search import Search
from datetime import datetime
import os, json, random
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps


VIEWS_FOLDER = os.environ.get('TAG_EARTH_VIEWS_FOLDER')
STYLES_FOLDER = os.environ.get('TAG_EARTH_STYLES_FOLDER')
JS_FOLDER = os.environ.get('TAG_EARTH_JS_FOLDER')
IMAGES_FOLDER = os.environ.get('TAG_EARTH_IMAGES_FOLDER')

def render_page_with_attributes(page, attributes):
    return template(os.path.join(VIEWS_FOLDER, page), **attributes)

def convert_date(string_date):
    return datetime.strptime(string_date, "%Y-%m-%d")

def compare_tiles_by_date(first_tile, second_tile):
    return cmp( convert_date(first_tile['date']), convert_date(second_tile['date']) )

def generate_random_path_row():
    path = random.randint(1, 233)
    row = random.randint(1, 248)
    return (path, row)

def get_random_tile():
    landsat_searcher = Search()

    (path, row) = generate_random_path_row()
    search_response = landsat_searcher.search(paths_rows="%d,%d" % (path, row), limit=100)
    while search_response['status'] != 'SUCCESS':
        print (path, row)
        (path, row) = generate_random_path_row()
        search_response = landsat_searcher.search(paths_rows="%d,%d" % (path, row), limit=100)

    tiles = search_response['results']
    tiles.sort( cmp = compare_tiles_by_date, reverse=True )
    return tiles[0]


plugin = MongoPlugin(uri="mongodb://127.0.0.1", db="tagEarth", json_mongo=True)
install(plugin)

@route('/')
def index():
    return render_page_with_attributes("index.html", get_random_tile())


@route('/submit_tags', method='POST')
def tag_tile(mongodb):
    submited_data = json.loads(request.forms.get('submission_data'))
    submited_data.update({'path': request.forms.get('path')})
    submited_data.update({'row': request.forms.get('row')})
    submited_data.update({'sceneID': request.forms.get('sceneID')})
    submited_data.update({'date': request.forms.get('date')})
    submited_data.update({'thumbnail': request.forms.get('thumbnail')})
    mongodb['tagged_scenes'].insert_one(submited_data)
    return render_page_with_attributes("submission_response.html", {})


@route('/tagged_scenes')
def list_tagged_scenes(mongodb):
    search_result = []
    for item in mongodb['tagged_scenes'].find():
        print item
        search_result.append(item)
    return render_page_with_attributes('list_tagged_scenes.html', {'tagged_scenes': search_result})


@route('/styles/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=STYLES_FOLDER, mimetype='text/css')


@route('/js/<filename:re:.*\.js>')
def send_jss(filename):
    return static_file(filename, root=JS_FOLDER, mimetype='text/javascript')


@route('/images/<filename:re:.*>')
def send_image(filename):
    return static_file(filename, root=IMAGES_FOLDER)

run(host='localhost', port='8080', reloader=True, debug=True)
