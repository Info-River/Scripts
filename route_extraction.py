import sys
from pyrosm import OSM
import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt


def dist(a, b):

    (x1, y1) = a

    (x2, y2) = b

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

class emergency_management:


    def __init__(self):
        self.vehicles=[]
        self.destinations=[]

        #Initialize OSM representation of geographic map
        osm=OSM("map.pbf")

        self.nodes, self.edges=osm.get_network(nodes=True,network_type="driving")
        self.node_dict=self.node_dict_generator(self.nodes)
        self.edges=self.add_new_score(self.edges)  #adds the custom score as edges

        #Create network
        self.G=osm.to_graph(self.nodes,self.edges,graph_type="networkx")

    def node_dict_generator(self,nodes):
        '''
        Function to generate a dictionary connecting node id to the respective coordinate
        :param nodes: geoDataFrame of node information
        :return: dictionary of nodes
        '''
        dict_node={}
        for index, row in nodes.iterrows():
            dict_node[row["id"]]=(row["lon"],row["lat"])

        return dict_node


    def emergency_route_pickup(self,end_coordinate):
        '''
        Function to make emergency routes, depending on type of emergency
        :param end_coordinate: incident coordinates - tuple (lonitude,latitude)
        :return: index of vehicles, list of edges the vehicle should follow to the incdent
        '''

        min_value=float("inf")
        min_route=[]
        chosen_vehicle_index=0

        for index, vehicle in enumerate(self.vehicles):
            start_coord=vehicle
            end_coord=end_coordinate
            #Selected the closest node in the map
            source_node=ox.distance.nearest_nodes(self.G,start_coord[0],start_coord[1])
            # print(source_node)
            end_node=ox.distance.nearest_nodes(self.G,end_coord[0],end_coord[1])
            route = nx.astar_path(self.G, source_node, end_node, weight="length")

            value_route=0
            i=0
            while i<len(route)-1:
                #Summing all the custom scores in each link
                value_route+=self.G.get_edge_data(route[i],route[i+1])[0]["custom_score"]
                i+=1

            if value_route<min_value:
                min_value=value_route
                min_route=route
                chosen_vehicle_index=index

        min_value = float("inf")
        min_route2 = []
        chosen_destination_index = 0

        for index, destination in enumerate(self.destinations):
            start_coord = end_coordinate
            end_coord = destination
            # Selected the closest node in the map
            source_node = ox.distance.nearest_nodes(self.G, start_coord[0], start_coord[1])
            end_node = ox.distance.nearest_nodes(self.G, end_coord[0], end_coord[1])
            route = nx.astar_path(self.G, source_node, end_node, weight="length")

            value_route = 0
            i = 0
            while i < len(route) - 1:
                # Summing all the custom scores in each link
                value_route += self.G.get_edge_data(route[i], route[i + 1])[0]["custom_score"]
                i += 1

            if value_route < min_value:
                min_value = value_route
                min_route2 = route
                chosen_destination_index = index


        #Conversion between node id to node coordinates
        route_coords=[]
        for road in min_route:
            route_coords.append(self.node_dict[road])
        for road in min_route2:
            route_coords.append(self.node_dict[road])

        # fig, ax = ox.plot_graph_route(self.G, min_route2, route_linewidth=6, node_size=0, bgcolor='k')

        # fig.savefig("big_route.png")

        # plt.show()

        return chosen_vehicle_index,chosen_destination_index,route_coords


    def add_vehicle(self,coords):
        '''
        Function to register vehicles to the system
        :param coords: co ordinates of the vehicle
        :return: None
        '''

        my_id=ox.distance.nearest_nodes(self.G,coords[0],coords[1])
        self.vehicles.append(coords)


    def add_desitnation(self,coords):
        my_id=ox.distance.nearest_nodes(self.G,coords[0],coords[1])
        self.destinations.append(coords)

    def add_new_score(self,edges):
        edges["custom_score"]=0
        edges["traffic_jam"]=0
        for index, row in edges.iterrows():

            #Randomly choose a trafic jam score between 0 and 10
            tj_score=random.randint(0,10)
            new_score=row["length"]*(1+tj_score)
            edges.loc[index,"custom_score"]=new_score
            edges.loc[index,"traffic_jam"]=tj_score
        return edges


my_city=emergency_management()



fake_hospital=(-8.64283,40.64720)
true_hospital=(-8.65504,40.63383)

my_city.add_desitnation(fake_hospital)
my_city.add_desitnation(true_hospital)

    #Adding agents
# my_city.add_vehicle((-8.65179,40.64380))
my_city.add_vehicle((-8.65179,40.64380))
my_city.add_vehicle(fake_hospital)
my_city.add_vehicle(true_hospital)
my_city.add_vehicle((-8.6436,40.6310))
my_city.add_vehicle((-8.6475,40.6333))
my_city.add_vehicle((-8.65413,40.63833))
my_city.add_vehicle((-8.6514,40.6277))
my_city.add_vehicle((-8.6371,40.6397))
my_city.add_vehicle((-8.6424,40.6456))



# print(my_city.vehicles)
    #End points
incident1=(-8.6581,40.6292)
incident2=(-8.6503,40.6302)
incident3=(-8.6530,40.6387)

    #Incident in a building
incident4=(-8.65459,40.64195)


    #Eventually add type
import time

#time the funciton call below
start_time = time.time()
print(my_city.emergency_route_pickup(incident4))
end_time = time.time()
print("Time taken: ",end_time-start_time)

# while(True):

    #TODO MQTT Listerner here:








    #TODO Send MQTT DATA

    # sys.sleep(100)


