import numpy as np
import networkx as nx
from itertools import combinations

def from_b_to_graph(binary_string, n):
    graph=nx.DiGraph()
    for i in range(len(binary_string)):
        if(binary_string[i]=="1"):
            source=int(i/(n-1))
            target=int(i%(n-1))
            if(target>=source):
                target+=1
            graph.add_edge(source,target)
    graph.add_nodes_from(range(n))
    return graph

def to_txt_a(graphs, n):
    with open(f"subgraphs_{n}.txt", "w") as file:
        print(f"n={n}", file=file)
        print(f"count={len(graphs)}", file=file)
        for i in range(len(graphs)):
            print(f"#{i+1}", file=file)
            edges = list(graphs[i][0].edges())
            for edge in edges:
                print(f"{edge[0]+1} {edge[1]+1}", file=file)

def to_txt_b(motifs, subgraphs):
    with open("count_motifs.txt", "w") as file:
        print(f"n={len(motifs)}", file=file)
        for i in range(len(motifs)):
            print(f"#{i+1}", file=file)
            print(f"count={motifs_count(motifs[i], subgraphs)}", file=file)

def not_isomorphic(new, graphs):
    edges=new.number_of_edges()
    for tuple in graphs:
        if tuple[1]==edges and nx.is_isomorphic(new, tuple[0]):
            return False
    return True

def create_all_graphs(n):
    if n==1:
        return [[nx.DiGraph(np.array([[1]])),1]]
    total=2**(n*(n-1))
    graphs_edges=[] #list of tuples (graph,graph.number_of_edges())
    for i in range(1,total):
        binary_string = bin(i)[2:]
        if(int(binary_string.count("1"))>=n-1): #check if the graph can be connected
            graph = from_b_to_graph(binary_string, n)
            if(nx.is_weakly_connected(graph) and not_isomorphic(graph, graphs_edges)):
                graphs_edges.append([graph,graph.number_of_edges()])
    return graphs_edges



def create_graph_from_file(n, file_name):
    graph=nx.DiGraph()
    with open(file_name, "r") as file:
        for line in file:
            edge = line.split()
            graph.add_edge(int(edge[0]) - 1, int(edge[1]) - 1)
    return graph

def motifs_count(motif, subgraphs):
    count = 0
    motif = nx.DiGraph(motif)
    for subgraph in subgraphs:
        if nx.is_isomorphic(motif, nx.DiGraph(subgraph)):
            count += 1
    return count

def get_subgraphs(graph, n):
    adj = nx.to_numpy_array(graph)
    subgraphs = []
    for combination in combinations(range(adj.shape[0]), n):
        subgraphs.append(adj[np.ix_(combination, combination)])
    return subgraphs



def ex_a():
    print("Please enter positive integer n:")
    n=int(input())
    graphs=create_all_graphs(n)
    to_txt_a(graphs, n)

def ex_b():
    print("Please enter positive integer n:")
    n=int(input())
    print("Please enter a txt file name (for the given graph):")
    file_name=input()
    graph = create_graph_from_file(n, file_name)
    if n > graph.number_of_nodes():
        print('Error: motif has more vertices than input graph')
        return
    motifs=create_all_graphs(n)
    subgraphs=get_subgraphs(graph, n)
    to_txt_b(motifs, subgraphs)




if __name__ == '__main__':


    for i in range(1, 6):
        print(dt.datetime.now())
        start = t.time()
        graphs = create_all_graphs(i)
        to_txt_a(graphs, i)
        end = t.time()
        print(f"n={i} time={dt.timedelta(seconds=end-start)}")
    print("Please enter the exercise number (a/b):")
    ex=input()
    if(ex=="a"):
        ex_a()
    elif(ex=="b"):
        ex_b()
    else:
        print("Error: invalid input")