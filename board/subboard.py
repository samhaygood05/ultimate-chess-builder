'''
Copyright 2024 Sam A. Haygood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pyvis.network import Network
from PIL import Image, ImageDraw
from tile import Tile
import math

class SubBoard:
    def __init__(self, name: str, subboard_type: str, tile_mappings: dict = {}, connection_mappings: dict = {}, **kwargs):
        self.name: str = name
        self.subboard_type: str = subboard_type
        self.tile_mappings: dict = tile_mappings.copy()
        self.connection_mappings: dict = connection_mappings
        self.graph = nx.MultiDiGraph()

        self.properties = {}

        if subboard_type == 'rectangular':
            self.properties['x'] = kwargs['x']
            self.properties['y'] = kwargs['y']
            self.properties['direction_mappings'] = 'default:rectangular'

            for i in range(self.properties['x']):
                for j in range(self.properties['y']):
                    # generate checkerboard coloring
                    color = 0xb2b2b2 if (i + j) % 2 == 0 else 0xe5e5e5

                    # generate the polygon square
                    polygon = [
                        (i, j),
                        (i + 1, j),
                        (i + 1, j + 1),
                        (i, j + 1)
                    ]

                    if len(tile_mappings) == 0:
                        self.tile_mappings[f'{name} ({i}, {j})'] = Tile(types=['default:normal'])

                        self.graph.add_node(f'{name} ({i}, {j})', tile=self.tile_mappings[f'{name} ({i}, {j})'], coord_pos=(i, j), color=color, polygon=polygon, tile_polygon=polygon)
                    elif f'{name} ({i}, {j})' in self.tile_mappings:
                        self.graph.add_node(f'{name} ({i}, {j})', tile=tile_mappings[f'{name} ({i}, {j})'], coord_pos=(i, j), color=color, polygon=polygon, tile_polygon=polygon)
            
            for i in range(self.properties['x']):
                for j in range(self.properties['y']):
                    # edge connections
                    edge_connections = [
                        ((i + 1, j), 'west'),
                        ((i - 1, j), 'east'),
                        ((i, j - 1), 'south'),
                        ((i, j + 1), 'north')
                    ]
                    
                    # vertex connections
                    vertex_connections = [
                        ((i + 1, j - 1), 'south-west'),
                        ((i - 1, j - 1), 'south-east'),
                        ((i + 1, j + 1), 'north-west'),
                        ((i - 1, j + 1), 'north-east')
                    ]

                    for connection in edge_connections:
                        if f'{name} ({connection[0][0]}, {connection[0][1]})' in self.graph.nodes:
                            self.graph.add_edge(f'{name} ({i}, {j})', f'{name} ({connection[0][0]}, {connection[0][1]})', direction=connection[1], type='edge')

                    for connection in vertex_connections:
                        if f'{name} ({connection[0][0]}, {connection[0][1]})' in self.graph.nodes:
                            self.graph.add_edge(f'{name} ({i}, {j})', f'{name} ({connection[0][0]}, {connection[0][1]})', direction=connection[1], type='vertex')
        elif subboard_type == 'hexagonal':
            self.properties['q'] = kwargs['q']
            self.properties['r'] = kwargs['r']
            self.properties['s'] = kwargs['s']
            self.properties['direction_mappings'] = 'default:hexagonal'

            size_x = self.properties['q'] // 2
            size_y = self.properties['r'] // 2
            size_z = self.properties['s'] // 2

            x_mod = self.properties['q'] % 2
            y_mod = self.properties['r'] % 2
            z_mod = self.properties['s'] % 2
            

            def hexagon(i, j):
                x = 3/2 * j + 3/2 * i
                y = math.sqrt(3)/2.0 * j - math.sqrt(3)/2.0 * i
                angles = [60*k*math.pi/180 for k in range(6)]
                hexagon = [(x + math.cos(angle), -y - math.sin(angle)) for angle in angles]
                return hexagon

            for q in range(-size_x, size_x + x_mod + 1):
                for r in range(-size_y, size_y + y_mod + 1):
                    for s in range(-size_z, size_z + z_mod + 1):
                        if q + r + s != 0:
                            continue
                        name = f'{self.name} ({q}, {r}, {s})'
                        # generate the checkerboard coloring
                        if (q - r) % 3 == 0:
                            color = 0xe5e5e5
                        elif (q - r) % 3 == 1:
                            color = 0xcccccc
                        else:
                            color = 0xb2b2b2

                        # generate the polygon hexagon
                        polygon = hexagon(r, s)

                        # generate the tile polygon, which is the bounding box of the hexagon
                        tile_polygon = [
                            (min(x for x, y in polygon), min(y for x, y in polygon)),
                            (max(x for x, y in polygon), min(y for x, y in polygon)),
                            (max(x for x, y in polygon), max(y for x, y in polygon)),
                            (min(x for x, y in polygon), max(y for x, y in polygon))
                        ]

                        if tile_mappings == {}:
                            self.tile_mappings[name] = Tile(types=['default:normal'])
                            self.graph.add_node(name, tile=self.tile_mappings[name], coord_pos=(q, r, s), color=color, polygon=polygon, tile_polygon=tile_polygon)
                            
                        elif name in tile_mappings:
                            self.graph.add_node(name, tile=tile_mappings[name], coord_pos=(q, r, s), color=color, polygon=polygon, tile_polygon=tile_polygon)

            for q in range(-size_x, size_x + x_mod + 1):
                for r in range(-size_y, size_y + y_mod + 1):
                    for s in range(-size_z, size_z + z_mod + 1):
                        if q + r + s != 0:
                            continue
                        name = f'{self.name} ({q}, {r}, {s})'
    
                        # edge connections
                        edge_connections = [
                            ((q, r-1, s+1), 'north'),
                            ((q+1, r-1, s), 'north-east-east'),
                            ((q+1, r, s-1), 'south-east-east'),
                            ((q, r+1, s-1), 'south'),
                            ((q-1, r+1, s), 'south-west-west'),
                            ((q-1, r, s+1), 'north-west-west')
                        ]

                        # vertex connections
                        vertex_connections = [
                            ((q+1, r-2, s+1), 'north-north-east'),
                            ((q+2, r-1, s-1), 'east'),
                            ((q+1, r+1, s-2), 'south-south-east'),
                            ((q-1, r+2, s-1), 'south-south-west'),
                            ((q-2, r+1, s+1), 'west'),
                            ((q-1, r-1, s+2), 'north-north-west')
                        ]

                        for connection in edge_connections:
                            if f'{self.name} ({connection[0][0]}, {connection[0][1]}, {connection[0][2]})' in self.graph.nodes:
                                self.graph.add_edge(name, f'{self.name} ({connection[0][0]}, {connection[0][1]}, {connection[0][2]})', direction=connection[1], type='edge')
                        
                        for connection in vertex_connections:
                            if f'{self.name} ({connection[0][0]}, {connection[0][1]}, {connection[0][2]})' in self.graph.nodes:
                                self.graph.add_edge(name, f'{self.name} ({connection[0][0]}, {connection[0][1]}, {connection[0][2]})', direction=connection[1], type='vertex')
        elif subboard_type == 'lone':
            self.properties['color'] = kwargs['color']
            self.properties['polygon'] = kwargs['polygon']
            self.properties['direction_mappings'] = kwargs['direction_mappings']
            self.graph.add_node(name, tile=tile_mappings[name], color=self.properties['color'], polygon=self.properties['polygon'])
        else:
            raise ValueError(f'Invalid subboard type: {subboard_type}')
        
        
    def preview_structure(self, filter: list = None, filter_blacklist: bool = False, use_pyvis: bool = False, name: str = None, **kwargs):
        if name == None:
            name = self.name

        filtered_graph = self.graph

        if 'internal_connections' in kwargs and kwargs['internal_connections']:
            for u, edges in self.connection_mappings.items():
                for edge in edges:
                    if edge['v'] in filtered_graph.nodes:
                        filtered_graph.add_edge(u, edge['v'], direction=edge['direction'], type=edge['type'])

        if 'external_connections' in kwargs and kwargs['external_connections']:
            for u, edges in self.connection_mappings.items():
                for edge in edges:
                    if edge['v'] not in filtered_graph.nodes:
                        filtered_graph.add_node(edge['v'], tile=Tile(types=['default:normal']), coord_pos=(0, 0), color=0xFFFFFF, polygon=[(0, 0), (1, 0), (1, 1), (0, 1)], tile_polygon=[(0, 0), (1, 0), (1, 1), (0, 1)])
                        filtered_graph.add_edge(u, edge['v'], direction=edge['direction'], type=edge['type'])

        # filter the graph to only include edges with a type in the filter list
        if filter != None:
            if filter_blacklist:
                filtered_graph = filtered_graph.edge_subgraph([edge for edge in filtered_graph.edges if filtered_graph.edges[edge]['type'] not in filter])
            else:
                filtered_graph = filtered_graph.edge_subgraph([edge for edge in filtered_graph.edges if filtered_graph.edges[edge]['type'] in filter])

        if use_pyvis:

            # strip the graph nodes of 'polygon' and 'tile' attributes
            for node in filtered_graph.nodes:
                filtered_graph.nodes[node].pop('polygon', None)
                filtered_graph.nodes[node].pop('tile', None)

            # create a network object
            net = Network(notebook=True, directed=True, height='100vh', width='100vw', bgcolor='#222222', font_color='white')
            net.from_nx(filtered_graph)

            # clear the edges in the network
            net.edges = []


            # assign a random color to each edge type
            edge_colors = {edge: f'#{np.random.randint(0, 0xFFFFFF):06x}' for edge in set([filtered_graph.edges[edge]['type'] for edge in filtered_graph.edges])}

            # assign the edge colors to the edges
            for u, v, data in filtered_graph.edges(data=True):  # Includes all edges, even parallel ones
                edge_type = data['type']  # Extract the type of the edge
                edge_direction = data['direction']
                color =edge_colors[edge_type]  # Get the corresponding color from the color map
                
                # Add the edge to the Pyvis network with the specific color
                net.add_edge(u, v, title=f"Type: {edge_type}\nDirection: {edge_direction}", color=color)

            # show the network
            return net.show(f'{name}.html')

        else:
            # draw the graph using spring layout
            pos = nx.spring_layout(filtered_graph)
            # add the name
            plt.title(name)
            nx.draw(filtered_graph, pos, with_labels=True, node_size=30, font_size=8, font_color='black')

    def preview_render(self, buffer = 0, resolution = (1080, 720), **kwargs):
        # Create a list of polygons and colors
        polygons = [(data['polygon'], data['tile'], data['tile_polygon'], data['color']) for node, data in self.graph.nodes(data=True)]
        # Find the bounding box of all polygons extended by the buffer
        min_x, min_y = np.inf, np.inf
        max_x, max_y = -np.inf, -np.inf
        for polygon, _, _, _ in polygons:
            xs, ys = zip(*polygon)
            min_x = min(min_x, min(xs))
            min_y = min(min_y, min(ys))
            max_x = max(max_x, max(xs))
            max_y = max(max_y, max(ys))
        
        # Apply buffer
        min_x -= buffer
        min_y -= buffer
        max_x += buffer
        max_y += buffer

        # Create figure and axis
        fig, ax = plt.subplots()
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal')

        zorder = 0

        # Create and add polygons with colors
        for polygon, _, _, hex_color in polygons:
            color = '#{0:06x}'.format(hex_color)
            patch = Polygon(polygon, closed=True, color=color, zorder=zorder)
            ax.add_patch(patch)
            zorder += 1

        if 'tiles' in kwargs and kwargs['tiles']:
            tile_texture_name = {tile: kwargs['tiles'][tile].texture_path for tile in kwargs['tiles']}

            for polygon, tile, tile_polygon, _ in polygons:
                # calculate the min and max x and y values of the tile_polygon
                min_x = min(x for x, y in tile_polygon)
                max_x = max(x for x, y in tile_polygon)
                min_y = min(y for x, y in tile_polygon)
                max_y = max(y for x, y in tile_polygon)
                # calculate the width and height of tile_polygon
                width = max_x - min_x
                height = max_y - min_y

                for type1 in tile.types:
                    texture_name = tile_texture_name[type1]
                    if texture_name != None:
                        namespace, name = texture_name.split(':')
                        img = Image.open(f'games/{namespace}/textures/tiles/{name}.png').convert('RGBA')
                        

                        # Convert the image to a NumPy array
                        img_array = np.array(img)

                        # normalize the polygon to have values between 0 and 1
                        normalized_polygon = [((x - min_x)/(max_x-min_x), (y - min_y)/(max_y-min_y)) for x, y in polygon]

                        # scale the polygon to the size of the image and convert the coordinates to integers
                        normalized_polygon = [(int(x * img.width), int(y * img.height)) for x, y in normalized_polygon]

                        # Create a mask for the tile polygon
                        mask = Image.new('L', (int(img.width), int(img.height)), 0)
                        ImageDraw.Draw(mask).polygon(normalized_polygon, outline=1, fill=1)
                        mask = np.array(mask)

                        # Apply the mask to the image
                        img_array[:, :, 3] = np.multiply(img_array[:, :, 3], mask)

                        # Add the image to the plot
                        ax.imshow(img_array, extent=(min_x, max_x, min_y, max_y), zorder=zorder)
                        zorder += 1
        if 'pieces' in kwargs and kwargs['pieces']:
            piece_texture_names = {piece: kwargs['pieces'][piece].texture_paths for piece in kwargs['pieces']}

            for polygon, tile, tile_polygon, _ in polygons:
                # calculate the min and max x and y values of the tile_polygon
                min_x = min(x for x, y in tile_polygon)
                max_x = max(x for x, y in tile_polygon)
                min_y = min(y for x, y in tile_polygon)
                max_y = max(y for x, y in tile_polygon)

                # calculate the width and height of tile_polygon
                width = max_x - min_x
                height = max_y - min_y

                if tile.piece != None:
                    try:
                        texture_name = piece_texture_names[tile.piece.piece_type][tile.piece.teams[0]]
                    except KeyError:
                        texture_name = piece_texture_names[tile.piece.piece_type]['default']
                    namespace, name = texture_name.split(':')
                    img = Image.open(f'games/{namespace}/textures/pieces/{name}.png').convert('RGBA')

                    # Convert the image to a NumPy array
                    img_array = np.array(img)

                    if 'teams' in kwargs:
                        team = kwargs['teams'][tile.piece.teams[0]]
                        hex_color = team.color # for example 0xff0000 is red
                        color = np.array([hex_color & 0xff, (hex_color & 0xff00) >> 8, (hex_color & 0xff0000) >> 16, 255]) / 255
                        img_array[:, :, :4] = np.multiply(img_array[:, :, :4], color)
                    
                    # normalize the polygon to have values between 0 and 1
                    normalized_polygon = [((x - min_x)/(max_x-min_x), (y - min_y)/(max_y-min_y)) for x, y in polygon]

                    # scale the polygon to the size of the image and convert the coordinates to integers
                    normalized_polygon = [(int(x * img.width), int(y * img.height)) for x, y in normalized_polygon]

                    # Create a mask for the tile polygon
                    mask = Image.new('L', (int(img.width), int(img.height)), 0)
                    ImageDraw.Draw(mask).polygon(normalized_polygon, outline=1, fill=1)
                    mask = np.array(mask)

                    # Apply the mask to the image
                    img_array[:, :, 3] = np.multiply(img_array[:, :, 3], mask)

                    ax.imshow(img_array, extent=(min_x, max_x, min_y, max_y), zorder=zorder)
                    zorder += 1


        # Set the size of your figure to match the resolution
        dpi = fig.get_dpi()
        fig.set_size_inches(resolution[1] / float(dpi), resolution[0] / float(dpi))

        # Remove axes for clarity
        ax.axis('off')

        # Show the plot
        plt.show()
