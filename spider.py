import csv
import time

import facebook
import networkx as nx
import matplotlib.pyplot as plt


token = "EAAGjLzQuFNcBANGc4ZBAeT3aY0j8hyfXi072fn9RoZBddQempQZA8NZAcRZAn81hNFskbb67jTk6ZBLmJbSbTYTS82VhmQswYe7NGN2UvobznWi96f3BQPqp4FPVhYtzCzKLDLEBFKD1uDqrli6GHbYUz8DehzQiii2DWTjrFlZBAZDZD"
team334 = "116920961670659"


class spider(object):
    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.graph = facebook.GraphAPI(access_token = token, version = version)

        self.edges = []
        self.nodes = []

        # Plug
        self. team334 = "116920961670659"

    def parse(self, data):
        '''Parses matrix read data from csv'''

        basket = []
        modified_data = []

        # Every blank line indicates the start of a new embeded lsit
        for n, x in enumerate(data):
            if(x == []):
                new_element = []
                for y in basket:
                    new_element += y
                modified_data.append(new_element)
                basket = []
            else:
                basket.append(x)
        # blank lists generate two
        for n, x in enumerate(modified_data):
            if x == []:
                modified_data.pop(n+1)
        return modified_data

    def save(self):
        '''Saves currrent data in 2 .csv files.
        '''
        # started = str(time.time())
        started = ''
        # Write nodes into csv.
        with open('nodes'+ started + '.csv', 'w') as f:
            writer = csv.writer(f, delimiter = '\n')
            writer.writerow(self.nodes)

        # Write Edges into csv.
        with open('edges' + started + '.csv', 'w') as f:
            writer = csv.writer(f, delimiter = '\n')
            for edge_list in self.edges:
                writer.writerow(edge_list)

    def read(self, **kwargs):
        '''Loads a file. Requires node_file and edge_file,
        both strings.
        '''
        # Read edge file and parse
        edges = []
        with open(kwargs['edge_file'], 'r') as f:
            reader = csv.reader(f, delimiter = '\n')
            edges = list(reader)
        self.edges = self.parse(edges)

        # Open and clean nodes.
        nodes = []
        with open(kwargs['node_file']) as f:
            reader = csv.reader(f, delimiter = '\n')
            for x in list(reader):
                nodes += x
        self.nodes = [x for x in nodes if x != []]
        # with open()

    def extract(self, iden):
        '''Gets the likes of a page and stores in object
        '''
        if iden in self.nodes:
            return False
        else:
            current_node = iden
            edges = []

            likes = self.graph.get_connections(current_node, connection_name = 'likes')

            for like in likes['data']:
                edges.append(like['id'])

            self.nodes.append(current_node)
            self.edges.append(edges)

            return edges

    def scrape(self, start_node, steps, **kwargs ):
        '''Scrape data from facebook'''
        ids = self.extract(start_node)
        stepped = 0

        # Collect data using the extract method.
        while stepped < steps and ids != []:
            new_ids = self.extract(ids.pop())
            print(len(self.edges[0]))
            # Ignore duplicate ids
            if new_ids is False:
                pass
            else:
                ids += new_ids
                stepped += 1

        # Save data if requested.
        if 'save' in kwargs:
            if kwargs['save']:
                self.save()
    def extract2(self, node):
        neighbors = self.graph.get_connections(node, connection_name = 'likes')
        return [x['id'] for x in neighbors['data']]
    def scrape2(self, start_node, steps, **kwargs):
        ids = self.extract2(start_node)
        stepped = 0

        while ids and stepped < steps:
            target = ids.pop(0)
            self.nodes.append(target)

            neighbors = self.extract2(target)
            self.edges.append(neighbors)

            for node in neighbors:
                if node not in ids:
                    ids.append(node)
            stepped += 1
    def make_network(self, **kwargs):
        '''Generates network from data'''

        G = nx.DiGraph() # Modeling a directed graph.
        nodes = self.nodes
        edges = self.edges

        # Make nodes.
        for edge_list in edges:
            G.add_nodes_from(edge_list, scraped = False)

        G.add_nodes_from(nodes, scraped = True) # Some scraped edges may have been explored as well.

        # Make edges.
        for node, edge_list in zip(nodes, edges):
            for node2 in edge_list:
                G.add_edge(node, node2)

        # Draw, if specified.
        if 'draw' in kwargs:
            if kwargs['draw']:
                pos = nx.spring_layout(G, k = .25, iterations = 10)

                # Draw with large bubbles and the names of pages
                if 'names' in kwargs:
                    if kwargs['name']:
                        # Scrape names.
                        labels = {}
                        # for iden in self.nodes:
                        #     name  = self.graph.get_object(iden, )
                        #     G[iden]['name'] = name
                        #     labels[iden] = name

                        # Drawing.
                        pos = nx.spring_layout(G, k = .5, iterations = 10)
                        nx.draw(G, pos, node_size = 100, width = .1)

                # Draw, color differently based on degree.
                else:
                    pos = nx.spring_layout(G, k = .15, iterations = 10)
                    degrees = list(G.out_degree(G.nodes()).values())

                    nx.draw(G, pos,
                        node_size = 10,
                        width = .1,
                        node_color = degrees,
                        cmap = plt.get_cmap('coolwarm'))

                # Save if requested.
                if 'save' in kwargs:
                    if kwargs['save']:
                        plt.savefig('graph' + str(time.time()) + '.png', dpi=1000)

                self.G = G
                plt.show()

    def oust(self, **kwargs):
        '''Prints current data'''

        if 'length' in kwargs:
            if kwargs['length']:
                print('----------------------------------')
                print("Nodes:", len(self.nodes))
                print("Edges:", len(self.edges))
                print('----------------------------------')
                return
        print('Scraped nodes')
        print(self.nodes)
        print('----------------------------------------------------------------')
        print('Edge lists')
        print(self.edges)



# s = spider(token, '2.7')

# s.scrape2(team334, 9, save = True)
# s.make_network(draw = True, save = True)

# s.read(node_file = 'nodes.csv', edge_file = 'edges.csv')
# s.make_network(draw = True)
