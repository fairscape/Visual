import sys
from pyld import jsonld
from pyld.jsonld import JsonLdError
import json
from flask import Flask, render_template, jsonify, request
import pandas as pd
from auth import *



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

EG_URL = os.environ.get("EG_URL","https://clarklab.uvarc.io/evidencegraph/")





app = Flask(__name__)
app.url_map.converters['everything'] = EverythingConverter



# send elements = [] containing nodes and edge
@app.route('/graph', methods=['GET'])
def hello():
    # GET method
    print("I was called!!!!")
    print(elements)
    cytoscape_elements = elements
    return jsonify(cytoscape_elements)


@app.route('/<everything:ark>')
@user_level_permission
def test_page(ark):
    global elements
    elements = []

    token = request.cookies.get("fairscapeAuth")

    data_jsonld = requests.get(EG_URL + ark, headers = {"Authorization": token}).json()

    if 'error' in data_jsonld.keys():
        return data_jsonld['error']
    try:
        try:
            data_jsonld_flat = jsonld.flatten(data_jsonld)  #
        except Exception as cause:
            raise JsonLdError(
                'Error flattening JSON-LD content ', cause)

        # print("\nflattened JSON-LD content\n", json.dumps(data_jsonld_flat, indent=2))

        elements = []  # contains nodes and edges
        nodes = []  # vertices
        edges = []  # links between vertices
        id_position = {}  # mapping of each @id to a number
        counter = 0

        # TODO: to check if http://schema.org/name missing
        for level in data_jsonld_flat:
            if level.get('@id') is None or '_:b' in level['@id']:  # flattening generates a blank node _:b when @id is missing
                print('Error: found blank node for missing @id at: ', level)
                sys.exit()
            if level.get(['@type'][0]) is None:
                print('Error: missing @type at: ', level)
                sys.exit()
            nodes_data = {}
            nodes_element = {}
            nodes_element['id'] = counter
            nodes_element['@id'] = level['@id']
            nodes_element['href'] = 'https://clarklab.uvarc.io/mds/' + level['@id']  # href in cytoscape to open as a URI
            nodes_element['@type'] = level['@type'][0]
            nodes_element['type'] = level['@type'][0]  # @type cannot be retrieved as node(@type)
            nodes_element['name'] = level['http://schema.org/name'][0]['@value']
            nodes_element['info'] = 'Name: ' + level['http://schema.org/name'][0]['@value'] + '\nType: ' + level['@type'][0] \
                                    + '\nPID: ' + level['@id']  # all attributes together
            nodes_data['data'] = nodes_element
            nodes.append(nodes_data)
            id_position[level['@id']] = counter
            counter += 1

        # print('\nNodes\n', json.dumps(nodes, indent=2))

        # populate edges
        for item in data_jsonld_flat:
            source_id = item['@id']  # chooses @id as source at each level for an edge
            for key, value in item.items():  # iterates through each flattened level
                if isinstance(value, list):
                    for i in value:
                        if isinstance(i, dict):
                            if '@id' in i.keys():
                                edges_data = {}
                                edges_element = {}
                                edges_element['source'] = id_position[source_id]
                                edges_element['target'] = id_position[i['@id']]
                                edges_element['label'] = key
                                edges_data['data'] = edges_element
                                edges.append(edges_data)

        # print('\nEdges\n', json.dumps(edges, indent=2))

        # copies all nodes and edges inside elements
        elements = nodes.copy()
        for element in edges:
            elements.append(element)

        # Convert multiple edges such that e1(v1, v2), e2(v1, v2), e3(v1, v2) =>
        # Multiples edges between v1, v2 such as http://schema.org/founder, http://schema.org/member become [founder, member]
        source = []
        target = []
        label = []
        for edge_data in edges:
            for edge in edge_data.values():
                for key, value in edge.items():
                    if key == 'source':
                        source.append(value)
                    if key == 'target':
                        target.append(value)
                    if key == 'label':
                        label.append(value)

        d = {'source': source, 'target': target, 'label': label}
        df = pd.DataFrame(data=d)

        # print('\nAll Edges\n', df)

        df_edge_has_common_nodes = df[df.duplicated(subset=['source', 'target'], keep=False)]
        # print('\nEdges with common nodes\n', df_edge_has_common_nodes)

        df_unique = df.drop_duplicates(subset=['source', 'target'], keep=False)
        # print('\nUnique Edges\n', df_unique)

        df_merged_edge_has_common_nodes = df_edge_has_common_nodes.groupby(['source', 'target'], as_index=False) \
            .agg({'label': ','.join})

        # print('\nMerged unique & non-unique edges\n', df_merged_edge_has_common_nodes)

        uri_prefix_suffix_dict_list = []  # Maps uri prefix to its suffix e.g. {http://schema.org/ : member"

        # populate common edge labels within [...] e.g. [founder, member, ...]
        def get_property_labels(labels):
            property_list = str(labels).split(',')
            if len(property_list) == 1:
                uri_prefix_suffix_dict = {}
                suffix = property_list[0].split('/')[-1]
                prefix = property_list[0].replace(suffix, '')
                uri_prefix_suffix_dict[prefix] = suffix
                uri_prefix_suffix_dict_list.append(uri_prefix_suffix_dict)
                return suffix
            elif len(property_list) > 1:
                property_list_size = len(property_list)
                # prop_list = []  # sending as a list does not add [] around the labels
                props_list = '['  # this string adds the anticipated []
                for prop in property_list:
                    uri_prefix_suffix_dict = {}
                    suffix = prop.split('/')[-1]
                    prefix = prop.replace(suffix, '')
                    uri_prefix_suffix_dict[prefix] = suffix
                    uri_prefix_suffix_dict_list.append(uri_prefix_suffix_dict)
                    # prop_list.append(suffix)
                    property_list_size -= 1
                    if property_list_size > 0:
                        props_list += suffix + ', '
                    else:
                        props_list += suffix
                # return prop_list
                return props_list + ']'


        elements = []  # reinitialize empty nodes and edges
        # Populate only unique edges which are not shared between two nodes
        for index, row in df_unique.iterrows():
            edge_data = {}
            edges_element = {}
            edges_element['source'] = row['source']
            edges_element['target'] = row['target']
            property_label = get_property_labels(row['label'])
            if property_label is None:
                print('ERROR: Could not find property label!')
                sys.exit()
            edges_element['label'] = property_label
            edge_data['data'] = edges_element
            elements.append(edge_data)

        # Populate only those edges which are shared between two vertices
        for index, row in df_merged_edge_has_common_nodes.iterrows():
            edge_data = {}
            edges_element = {}
            edges_element['source'] = row['source']
            edges_element['target'] = row['target']
            property_labels = get_property_labels(row['label'])
            if property_labels is None:
                print('ERROR: Could not find property labels!')
                sys.exit()
            edges_element['label'] = property_labels
            edge_data['data'] = edges_element
            elements.append(edge_data)

        # print('\nRefined Edges\n', elements)


        # Adding the nodes
        def is_node_in_edges(node, edges):
            edge_nodes = set()
            for edge_data_value in edges:
                edge_nodes.add(edge_data_value['data']['source'])
                edge_nodes.add(edge_data_value['data']['target'])
            if node['data']['id'] in edge_nodes:
                return True
            else:
                return False


        for node in nodes:
            if is_node_in_edges(node, edges):
                elements.append(node)
    except:
        return "Visual Failed. Probably missing type, name, or ID"
    print('Made it to render.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
