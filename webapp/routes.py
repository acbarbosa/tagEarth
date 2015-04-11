# -*- coding: utf-8 -*-
from bottle import route, run, template
from landsat.search import Search
from datetime import datetime
import os, json, random

VIEWS_FOLDER = os.environ.get('TAG_EARTH_VIEWS_FOLDER')


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


def get_tags():
    return [
        {'name': "Cloudy"}, 
        {'name': "Desert"},
        {'name': "fire"},
        {'name': "fog"},
        {'name': "geiser"},
        {'name': "glacier"},
        {'name': "hill"},
        {'name': "ice"},
        {'name': "iceberg"},
        {'name': "island"},
        {'name': "lagoon"},
        {'name': "lake"},
        {'name': "mountains"},
        {'name': "ravine"},
        {'name': "river"},
        {'name': "sea"},
        {'name': "urban area"},
        {'name': "vegetation"},
        {'name': "volcano"}
    ]


@route('/')
def index():
    page_model = get_random_tile()
    page_model.update({'tags': get_tags()})
    print(page_model)
    return render_page_with_attributes("index.html", page_model)

run(host='localhost', port='8080', reloader=True, debug=True)
