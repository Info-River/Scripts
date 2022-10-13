#import fiona
from pyrosm import OSM, get_data
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import random 

from ambulance import ambulance
from cop import cop
from firefighter import firefighter as fire_f
from hospital import hospital


import matplotlib.pyplot as plt
import uuid
import pandas as pd


class emergency_management:


    def __init__(self):

        #fp=get_data("map.osm")

        self.list_cops=[]
        self.list_ambulances=[]
        self.list_firefighters=[]
        self.list_hospital=[]

        self.agent_dict={}

        #Initialize OSM representation of geographic map
        osm=OSM("map.pbf")

        #TODO Create bounding box 


        self.nodes, self.edges=osm.get_network(nodes=True,network_type="driving")    

        self.node_dict=self.node_dict_generator(self.nodes)
        

        self.edges=self.add_new_score(self.edges)

        #Create network 
        self.G=osm.to_graph(self.nodes,self.edges,graph_type="networkx")


        
        

        #source_node=ox.distance.nearest_nodes(G,self.main_hospital[0],self.main_hospital[1])
        #end_incident4=ox.distance.nearest_nodes(G,self.incident4[0],self.incident4[1])
#
        ##route = nx.shortest_path(G, source_node, end_incident4, weight="length")
        #print(route)


    def node_dict_generator(self,nodes):
        #Function to generate a dictionary connecting node id to the respective coordinate
        #nodes - geoDataFrame of node information

        dict_node={}
        for index, row in nodes.iterrows():
            dict_node[row["id"]]=(row["lon"],row["lat"])

        return dict_node


    def emergency_route(self,end_coordinate,type_emerg):
        #Function to make emergency routes, depending on type of emergency
        # end_coordinate - incident coordinates - tuple (lonitude,latitude)
        # type_emerg - type of emegency - strin        


        actors=[]
        #A list will made with all the emergency actors available a suited for the incident
        #NOTE for now, only considering shutout event
        if type_emerg=="shutout":
            actors=self.list_cops

        min_value=float("inf")
        #min_value=0
        min_route=[]
        chosen_actor=None

        for actor in actors:
            start_coord=actor.coords
            end_coord=end_coordinate
            #Selected the closest node in the map
            source_node=ox.distance.nearest_nodes(self.G,start_coord[0],start_coord[1])
            end_node=ox.distance.nearest_nodes(self.G,end_coord[0],end_coord[1])
            route = nx.shortest_path(self.G, source_node, end_node, weight="length")

            #Score Calculation
            #print("start")
            #list_nodes=nx.nodes(self.G)
            #print(list_nodes)
            #if actor.id in list_nodes:
            #    print("woah")
            #input()
            value_route=0
            i=0
            while i<len(route)-1:
                
                #Summing all the custom scores in each link
                value_route+=self.G.get_edge_data(route[i],route[i+1])[0]["custom_score"]
                #print(self.edges.loc[(self.edges["u"]==route[i]) & (self.edges["v"]==route[i+1]),"custom_score"].item())
                

                #value_route+=self.edges.loc[(self.edges["u"]==route[i]) & (self.edges["v"]==route[i+1]),"custom_score"].item()
                i+=1
                
            if value_route<min_value:
                min_value=value_route
                min_route=route
                chosen_actor=actor

        
        #Conversion between node id to node coordinates
        route_coords=[]
        for road in min_route:
            route_coords.append(self.node_dict[road])

        print(route_coords)


      
        fig, ax = ox.plot_graph_route(self.G, min_route, route_linewidth=6, node_size=0, bgcolor='k')

        fig.savefig("big_route.png")
        
        plt.show()
        input()
        print(route)



    def add_agent(self,coords,type_agent):
        #Function to register agetns to the system


        my_id=ox.distance.nearest_nodes(self.G,coords[0],coords[1])

        self.agent_dict[my_id]=coords

        if type_agent=="fire":
            self.list_firefighters.append(fire_f(coords,my_id))
        elif type_agent=="cop":
            self.list_cops.append(cop(coords,my_id))
        elif type_agent=="ambulance":
            self.list_ambulances.append(ambulance(coords,my_id))

    def add_hospital(self,coords):
        my_id=ox.distance.nearest_nodes(self.G,coords[0],coords[1])
        
        self.agent_dict[my_id]=coords
        self.list_hospital.append(hospital(coords))

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