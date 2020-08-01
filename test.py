import sys
from pyld import jsonld
from pyld.jsonld import JsonLdError
import json
from flask import Flask, render_template, jsonify
import pandas as pd

JSONLD_FILE_PATH = 'static/jsonld-data/jsonld-sample4.json'
try:
    file = open(JSONLD_FILE_PATH, 'rb')
except OSError:
    print("Error: Could not open/read file:", JSONLD_FILE_PATH)
    sys.exit()

with file as file_jsonld:
    try:
        data_jsonld = json.load(file_jsonld)  # JSON-LD content
    except ValueError:
        print('Error loading file as JSON!')



# print('\nNodes and Edges\n', elements)

import sys,os
from pyld import jsonld
from pyld.jsonld import JsonLdError
import json
from flask import Flask, render_template, jsonify
import pandas as pd
from werkzeug.routing import PathConverter
import requests

class EverythingConverter(PathConverter):
    regex = '.*?'

EG_URL = os.environ.get("EG_URL","http://eg/eg/")





app = Flask(__name__)
app.url_map.converters['everything'] = EverythingConverter



# send elements = [] containing nodes and edge
@app.route('/graph', methods=['GET'])
def hello():
    # GET method
    print(elements)
    cytoscape_elements = elements
    return jsonify(cytoscape_elements)


@app.route('/<everything:ark>')
def test_page(ark):
    global elements
    elements = [{'data': {'source': 0, 'target': 4, 'label': 'generatedBy'}}, {'data': {'source': 1, 'target': 0, 'label': 'usedDataset'}}, {'data': {'source': 1, 'target': 2, 'label': 'usedSoftware'}}, {'data': {'source': 2, 'target': 7, 'label': 'author'}}, {'data': {'source': 3, 'target': 1, 'label': 'generatedBy'}}, {'data': {'source': 4, 'target': 5, 'label': 'usedDataset'}}, {'data': {'source': 4, 'target': 6, 'label': 'usedSoftware'}}, {'data': {'source': 5, 'target': 7, 'label': 'author'}}, {'data': {'source': 6, 'target': 7, 'label': 'author'}}, {'data': {'id': 0, '@id': 'ark:99999/496b5ab9-1fd9-4d76-8e00-fb3a616313c1', 'href': 'ark:99999/496b5ab9-1fd9-4d76-8e00-fb3a616313c1', '@type': 'http://schema.org/Dataset', 'type': 'http://schema.org/Dataset', 'name': 'part-00000-6ad57486-fa4e-4ef7-9690-2d3a9151a08d-c000.csv', 'info': 'Name: part-00000-6ad57486-fa4e-4ef7-9690-2d3a9151a08d-c000.csv\nType: http://schema.org/Dataset\nPID: ark:99999/496b5ab9-1fd9-4d76-8e00-fb3a616313c1'}}, {'data': {'id': 1, '@id': 'ark:99999/6312878c-a2ed-4b83-b298-6c7f16538815', 'href': 'ark:99999/6312878c-a2ed-4b83-b298-6c7f16538815', '@type': 'http://purl.org/evi/Computation', 'type': 'http://purl.org/evi/Computation', 'name': 'Computation', 'info': 'Name: Computation\nType: http://purl.org/evi/Computation\nPID: ark:99999/6312878c-a2ed-4b83-b298-6c7f16538815'}}, {'data': {'id': 2, '@id': 'ark:99999/6698fe15-edac-41b1-b45b-ae4e5124d862', 'href': 'ark:99999/6698fe15-edac-41b1-b45b-ae4e5124d862', '@type': 'http://schema.org/SoftwareSourceCode', 'type': 'http://schema.org/SoftwareSourceCode', 'name': 'Image Script', 'info': 'Name: Image Script\nType: http://schema.org/SoftwareSourceCode\nPID: ark:99999/6698fe15-edac-41b1-b45b-ae4e5124d862'}}, {'data': {'id': 3, '@id': 'ark:99999/7681ef7e-82bf-4fa1-913a-f1870d8203ea', 'href': 'ark:99999/7681ef7e-82bf-4fa1-913a-f1870d8203ea', '@type': 'http://schema.org/Dataset', 'type': 'http://schema.org/Dataset', 'name': 'Histogram_Heatmap.png', 'info': 'Name: Histogram_Heatmap.png\nType: http://schema.org/Dataset\nPID: ark:99999/7681ef7e-82bf-4fa1-913a-f1870d8203ea'}}, {'data': {'id': 4, '@id': 'ark:99999/a86cc2b6-6c3d-4dde-a8a0-ba84c49f8082', 'href': 'ark:99999/a86cc2b6-6c3d-4dde-a8a0-ba84c49f8082', '@type': 'http://purl.org/evi/Computation', 'type': 'http://purl.org/evi/Computation', 'name': 'Computation', 'info': 'Name: Computation\nType: http://purl.org/evi/Computation\nPID: ark:99999/a86cc2b6-6c3d-4dde-a8a0-ba84c49f8082'}}, {'data': {'id': 5, '@id': 'ark:99999/c00d2f61-3943-4187-8ae4-f063ae99c56f', 'href': 'ark:99999/c00d2f61-3943-4187-8ae4-f063ae99c56f', '@type': 'http://schema.org/Dataset', 'type': 'http://schema.org/Dataset', 'name': 'Raw Data', 'info': 'Name: Raw Data\nType: http://schema.org/Dataset\nPID: ark:99999/c00d2f61-3943-4187-8ae4-f063ae99c56f'}}, {'data': {'id': 6, '@id': 'ark:99999/ebbbd304-8c8c-40bb-8e91-dc4e3157c813', 'href': 'ark:99999/ebbbd304-8c8c-40bb-8e91-dc4e3157c813', '@type': 'http://schema.org/SoftwareSourceCode', 'type': 'http://schema.org/SoftwareSourceCode', 'name': 'Processing  Script', 'info': 'Name: Processing  Script\nType: http://schema.org/SoftwareSourceCode\nPID: ark:99999/ebbbd304-8c8c-40bb-8e91-dc4e3157c813'}}, {'data': {'id': 7, '@id': 'https://orcid.org/0000-0002-1103-3882', 'href': 'https://orcid.org/0000-0002-1103-3882', '@type': 'http://schema.org/Person', 'type': 'http://schema.org/Person', 'name': 'Justin Niestroy', 'info': 'Name: Justin Niestroy\nType: http://schema.org/Person\nPID: https://orcid.org/0000-0002-1103-3882'}}]
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
