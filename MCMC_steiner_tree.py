import pandas as pd
import random
import networkx as nx
import re
import numpy as np
import timeit


def pre_pros(df):
    dic_incidence = {}
    dic_edges = {}
    G = []
    for ix in df.index:
        s, t, w = df.loc[ix]["SOURCE TARGET WEIGHT".split()]
        u = sorted({s, t})
        G.append(u)
        dic_edges[str(u)] = w
        for i, u in enumerate([s, t]):
            if u not in dic_incidence.keys():
                dic_incidence[u] = [[s, t][(i + 1) % 2]]
            else:
                dic_incidence[u].append([s, t][(i + 1) % 2])
    
    for k, v in dic_incidence.items():
      dic_v = {n: dic_edges[str(sorted({k, n}))] for n in v}
      v = dict(sorted(dic_v.items(), key=lambda x: x[1], reverse=False)).keys()
      dic_incidence[k] = list(v)

    df_G = pd.DataFrame(dic_incidence.items(), columns="NODE NB".split()).set_index("NODE")
    return df_G, dic_incidence, dic_edges, G


def get_N(u, df, greedy=False):
    N = df.loc[u]["NB"].copy()
    if not greedy:
      random.shuffle(N)
    return N


def BFS(p, list_e, E, df):
    visited = [p]
    U = []
    for n in get_N(p, df):
        if (sorted({n, p}) in E) and all([sorted({n, p}) != e for e in list_e]):
            U.append(n)
    while U:
        u = U.pop(0)
        if u not in visited:
            visited.append(u)
            for n in get_N(u, df):
                if (sorted({n, u}) in E) and all([sorted({n, u}) != e for e in list_e]):
                    U.append(n)
    return visited


def random_path(s, list_e, S, df, dic_edges, greedy=False, approach="BFS"):
    visited = [s]
    paths = {s: ''}
    U = []

    for n in get_N(s, df, greedy):
        if all([sorted({n, s}) != e for e in list_e]):
            paths[n] = s
            U.append(n)

    t = None
    while U:
        ix = 0
        if approach == "DFS":
          ix = -1
        elif approach == "random":
          ix = np.random.randint(len(U))
        u = U.pop(ix)
        if u not in visited:
            visited.append(u)
            for n in get_N(u, df, greedy):
                if all([sorted({n, u}) != e for e in list_e]):
                    U.append(n)
                    if n in S:
                        U = []
                        t = n
                    if n not in visited:
                        paths[n] = u
    path = {'*': t}
    v = t
    while v in paths.keys():
        u = paths[v]
        path[v] = u
        v = u
    return path


def print_path(path):
    v = path['*']
    o = v
    s = path[v]
    while s != '':
        o += ' >- ' + s
        s = path[s]
    print(o[::-1])


def edges_path(path):
    E = []
    s = path['*']
    t = path[s]
    E.append(sorted({s, t}))
    s = t
    while s != '':
        t = path[s]
        if t != "":
            E.append(sorted({s, t}))
        s = t
    return E


def plot_graph_by_edges(F, G, terminals, seed=0):
    grafo_test = nx.Graph()
    for u in G:
        u0, u1 = u
        if u in F:
            grafo_test.add_edge(u0, u1, color="red")
        else:
            grafo_test.add_edge(u0, u1, color="gray")

    c_nodes = []
    used_nodes = [item for sublist in F for item in sublist]
    for n in grafo_test.nodes:
        c = 'tab:purple' if n in terminals else 'tab:blue'
        if n not in used_nodes:
            c = 'lightgray'
        c_nodes.append(c)

    colors = nx.get_edge_attributes(grafo_test, 'color').values()
    pos = nx.spring_layout(grafo_test, seed=seed)
    return nx.draw(grafo_test, pos, edge_color=colors, node_color=c_nodes, with_labels=True)


def Kruskal(V, dic_E):
    U = []
    leaves = V.copy()
    NB = {}
    union_find = {}
    for v in V:
        union_find[v] = [v, 1]

    def find(x):
        while union_find[x][0] != x:
            x = union_find[x][0]
        return x

    def union(x, y):
        x, y = find(x), find(y)
        if x != y:
            if union_find[x][1] < union_find[y][1]:
                (x, y) = (y, x)

            union_find[y][0] = x
            union_find[x][1] += union_find[y][1]

    sorted_edges = sorted(dic_E.items(), key=lambda x: x[1], reverse=False)
    for (u, _) in sorted_edges:
        u0, u1 = eval(u)
        f0, f1 = find(u0), find(u1)
        if f0 != f1:
            U.append(sorted({u0, u1}))

            for i in [0, 1]:
                ui = [u0, u1][i]
                ui_1 = [u0, u1][(i + 1) % 2]
                if union_find[[f0, f1][i]][1] > 1:
                    leaves.discard(ui)
                if ui not in NB.keys():
                    NB[ui] = [ui_1]
                else:
                    NB[ui].append(ui_1)

            union(u0, u1)

    return U, leaves, NB


def Trans(v, x, NB_x, df_NB, dic_edges, terminals, greedy=False, path_approach="BFS", remove_approach="edge"):
    threshold = 100
    # remove random edge   
    def remove_edge(): 
      hat_u = []
      RP_a = {}
      ix = int(np.floor(v * len(x)))
      b0 = True
      while b0:
          hat_u = x[ix]
          b, a = min(hat_u), max(hat_u)
          CC_b = BFS(b, [hat_u], x, df_NB)
          RP_a = random_path(a, hat_u, CC_b, df_NB, dic_edges, greedy, path_approach)
          b0 = (RP_a["*"] == None)
          ix = (ix+1)%len(x)
      return RP_a, [hat_u]

    # remove random vertex with degree 2
    def remove_node():
      ix = int(np.floor(v * len(NB_x)))
      hat_node = -1
      hat_u1 = []
      hat_u2 = []
      RP_a = {}
      b0 = True
      t = 0
      while b0 and (t<threshold):
          t+=1
          hat_node = list(NB_x.keys())[ix]
          b0 = ((len(NB_x[hat_node]) != 2) or (hat_node in terminals))
          if not b0:
            hat_u1 = sorted({hat_node, NB_x[hat_node][0]})
            hat_u2 = sorted({hat_node, NB_x[hat_node][1]})
            
            b = hat_u1[hat_u1[0] == hat_node]
            a = hat_u2[hat_u2[0] == hat_node]
            CC_b = BFS(b, [hat_u1, hat_u2], x, df_NB)
            RP_a = random_path(a, [hat_u1, hat_u2], CC_b, df_NB, dic_edges, greedy, path_approach)
            b0 = (RP_a["*"] == None)
          if b0:
            ix = (ix+1)%len(NB_x)
      return b0, RP_a, [hat_u1, hat_u2]

    vp = 0
    if remove_approach == "node":
      vp = 1
    elif remove_approach == "random":
      vp = 1/2

    if np.random.uniform() < vp:
      b0, RP_a, list_remove = remove_node()
      if b0:
        RP_a, list_remove = remove_edge()
    else:
      RP_a, list_remove = remove_edge()

    x1 = x.copy()

    for u in list_remove:
       x1.remove(u)

    # print(RP_a)
    # print(hat_node)
    # print(list_remove)
    for u in edges_path(RP_a):
        x1.append(u)

    V = set()
    dic_E = {}
    for u in x1:
        V = V.union(u)
        dic_E[str(sorted(u))] = dic_edges[str(sorted(u))]

    x2, leaves, NB_y = Kruskal(V, dic_E)
    y = x2.copy()
    for l in leaves:
        if l not in terminals:
            n = l
            while (len(NB_y[n]) == 1) and (n not in terminals):
                p = NB_y[n][0]
                y.remove(sorted({n, p}))
                NB_y.pop(n)
                NB_y[p].remove(n)
                n = p
    return y, NB_y


def weight(x, dic_edges):
    s = 0
    for u in x:
        s += dic_edges[str(sorted(u))]
    return s


class Annealing(object):
    def __init__(self, nf, beta, df_NB_G, dic_weight_edges, terminals, greedy=False, path_approach="BFS", remove_approach="edge"):
        self.nf = nf
        self.beta = beta
        self.CM = []
        self.times = []
        self.X = []

        self.greedy =greedy
        self.path_approach = path_approach
        self.remove_approach = remove_approach

        self.V = set(df_NB_G.index)
        self.df_NB_G = df_NB_G
        self.dic_weight_edges = dic_weight_edges
        self.terminals = terminals

    def estado_inicial(self):
        x0, _, NB_x0 = Kruskal(self.V, self.dic_weight_edges)
        return x0, NB_x0

    def Trans(self, v, x, NB_x):
        return Trans(v, x, NB_x, self.df_NB_G, self.dic_weight_edges, self.terminals, self.greedy, self.path_approach, self.remove_approach)

    def coef_R(self, x, y, beta):
        sum_x = sum([self.dic_weight_edges[str(u)] for u in x if u not in y])
        sum_y = sum([self.dic_weight_edges[str(u)] for u in y if u not in x])
        dif = sum_y-sum_x
        return np.exp(-beta * dif)

    def MCMC(self, u, v, save_rate=100):
        start = timeit.default_timer()
        x0, NB_x0 = self.estado_inicial()
        CM = [x0]
        times = [0]
        (xn_1, NB_xn_1) = (x0, NB_x0)
        for n, un in enumerate(u):
            vn = v[n]
            y, NB_y = self.Trans(vn, xn_1, NB_xn_1)
            if un <= self.coef_R(xn_1, y, self.beta(n)):
                (xn_1, NB_xn_1) = (y, NB_y)
            if (n % save_rate == 0) or (n == self.nf - 1):
                stop = timeit.default_timer()
                CM.append(xn_1)
                times.append(stop-start)
        self.CM = CM
        self.X = CM[-1]
        self.times = times


def read_stp(file_name):
    with open(file_name) as f:
        lines = f.readlines()

        sections = "Comment Graph Terminals".split()
        current_section = ""
        n, m = 0, 0
        col_s = []  # node source
        col_t = []  # node target
        col_w = []  # weight fun
        terminals = []
        for l in lines:
            if "SECTION" in l:
                current_section = l.replace("SECTION", "").strip()
            elif "END" in l:
                current_section = ""
            elif current_section == "Graph":
                if "Nodes" in l:
                    n = int(re.findall(r"\d+", l)[0])
                elif "Edges" in l:
                    m = int(re.findall(r"\d+", l)[0])
                elif "E" in l:
                    s, t, w_st = re.findall(r"\d+", l)
                    s, t, w_st = int(s), int(t), int(w_st)
                    col_s.append(s)
                    col_t.append(t)
                    col_w.append(w_st)
            elif current_section == "Terminals":
                if "T " in l:
                    terminals.append(int(re.findall(r"\d+", l)[0]))

        df_edges_G = pd.DataFrame({
            "SOURCE": col_s,
            "TARGET": col_t,
            "WEIGHT": col_w
        })

        return df_edges_G, terminals


def check_steiner_tree(x, dic_edges, terminals, G):
    V = set()
    dic_E = {}
    for u in x:
        V = V.union(u)
        dic_E[str(sorted(u))] = dic_edges[str(sorted(u))]
    return (Kruskal(V, dic_E)[0] == x) and set(terminals).issubset(set(V)) and all([(e in G) for e in x])

