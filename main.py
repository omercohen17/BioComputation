import numpy as np
import networkx as nx
from itertools import combinations

def from_b_to_graph(binary_list, n):

    matrix=np.zeros((n,n))
    for i in range(len(binary_list)):
        if(binary_list[i]==1):
            source=int(i/(n-1))
            target=int(i%(n-1))
            if(target>=source):
                target+=1

            matrix[source,target]=1
    return nx.DiGraph(matrix)

def to_txt_a(graphs, n):
    with open(f"subgraphs_{n}.txt", "w") as file:
        print(f"n={n}", file=file)
        print(f"count={len(graphs)}", file=file)
        for i in range(len(graphs)):
            print(f"#{i+1}", file=file)
            edges = list(graphs[i].edges())
            for edge in edges:
                print(f"{edge[0]+1} {edge[1]+1}", file=file)

def to_txt_b(motifs, subgraphs):
    with open("count_motifs.txt", "w") as file:
        print(f"n={len(motifs)}", file=file)
        for i in range(len(motifs)):
            print(f"#{i+1}", file=file)
            print(f"count={motifs_count(motifs[i], subgraphs)}", file=file)

def not_isomorphic(new, graphs):
    for graph in graphs:
        if nx.is_isomorphic(new, graph):
            return False
    return True

def create_all_graphs(n):
    if n==1:
        return [nx.DiGraph(np.array([[1]]))]
    total=n*(n-1)
    graphs=[]
    for i in range(1,2**total):
        binary_string = bin(i)[2:].zfill(total)
        binary_list = [int(bit) for bit in binary_string]
        if(binary_list.count(1)>=n-1): #check if the graph can be connected
            graph = from_b_to_graph(binary_list, n)
            if(nx.is_weakly_connected(graph) and not_isomorphic(graph, graphs)):
                graphs.append(graph)

    return graphs



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
    print("Please enter the exercise number (a/b):")
    ex=input()
    if(ex=="a"):
        ex_a()
    elif(ex=="b"):
        ex_b()
    else:
        print("Error: invalid input")



