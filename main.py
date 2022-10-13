#import fiona
from pyrosm import OSM, get_data
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import random 

from emergency_management import emergency_management as em





def main():
    
    my_city=em()



    fake_hospital=(-8.64283,40.64720)
    true_hospital=(-8.65504,40.63383)

    my_city.add_hospital(fake_hospital)
    my_city.add_hospital(true_hospital)

    #Adding agents
    my_city.add_agent((-8.65179,40.64380),"fire")
    my_city.add_agent(fake_hospital,"ambulance")
    my_city.add_agent(true_hospital,"ambulance")
    my_city.add_agent((-8.6436,40.6310),"ambulance")
    my_city.add_agent((-8.6475,40.6333),"ambulance")
    my_city.add_agent((-8.65413,40.63833),"cop")
    my_city.add_agent((-8.6514,40.6277),"cop")
    my_city.add_agent((-8.6371,40.6397),"cop")
    my_city.add_agent((-8.6424,40.6456),"cop")

    #End points
    incident1=(-8.6581,40.6292)
    incident2=(-8.6503,40.6302)
    incident3=(-8.6530,40.6387)

    #Incident in a building
    incident4=(-8.65459,40.64195)


    #Eventually add type
    my_city.emergency_route(incident4,"shutout")



    #Find nearest node to startingpoint

    #NOTE just experimenting on find shortest path 

    #source_node=ox.distance.nearest_nodes(G,main_hospital[0],main_hospital[1])
    #end_incident4=ox.distance.nearest_nodes(G,incident4[0],incident4[1])
#
    #route = nx.shortest_path(G, source_node, end_incident4, weight="length")
    #fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')





    #print(G)
#
    #ox.plot_graph(G)
    #plt.show()


    #drive_net = osm.get_network(network_type="driving")
    #drive_net.plot()
#
    #plt.show()











if __name__=="__main__":
    main()




