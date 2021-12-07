import pandas as pd
import numpy as np
from MCMC_steiner_tree import Annealing, pre_pros, plot_graph_by_edges, Trans, weight, Annealing, read_stp, check_steiner_tree
import pickle
import json
import os

df_opt = pd.read_excel('Testset_I320.xlsx', sheet_name="I080")
df_opt = df_opt.set_index("Name")

stp_names = ['i080-001.stp', 'i080-011.stp', 'i080-021.stp', 'i080-031.stp', 'i080-041.stp', 'i080-101.stp',
             'i080-111.stp', 'i080-121.stp', 'i080-131.stp', 'i080-141.stp', 'i080-201.stp', 'i080-211.stp',
             'i080-221.stp', 'i080-231.stp', 'i080-241.stp', 'i080-301.stp', 'i080-311.stp', 'i080-321.stp',
             'i080-331.stp', 'i080-341.stp']

# CREATE FOLDER -> you need to create folder called "gridsearch"
# parent_dir = r"C:\Users\felip\PycharmProjects\steiner-tree-annealing\gridsearch"
# for stp_name in stp_names:
#     directory = stp_name.replace(".stp", "")
#     path = os.path.join(parent_dir, directory)
#     os.mkdir(path)

# DO NOT TOUCH IT
# params = {
#     "nf": 3000,
#     "save_rate": 5,
#     "repeat": 10
# }
#
# with open("gridsearch/"+'params.json', 'w') as f:
#     json.dump(params, f)
#
# gridsearch = {
#     "a": list(np.linspace(0.5, 2, num=5)),
#     "b": list(np.linspace(0, 1, num=5))
# }
#
# with open("gridsearch/" + 'gridsearch.json', 'w') as f:
#     json.dump(gridsearch, f)
#
# UNIFORMS = [
#             (np.random.uniform(size=params["nf"]),
#              np.random.uniform(size=params["nf"]))
#             for _ in range(params["repeat"])
#             ]
#
# with open("gridsearch/" + "UNIFORMS.pickle", "wb") as f:
#     pickle.dump(np.array(UNIFORMS), f)

# LOAD params, gridsearch, uniforms (TO USE SAME "RANDOMNESS")
with open("gridsearch/"+'params.json', ) as f:
    params = json.load(f)
with open("gridsearch/"+'gridsearch.json', ) as f:
    gridsearch = json.load(f)
with open("gridsearch/" + "UNIFORMS.pickle", "rb") as f:
    UNIFORMS = pickle.load(f)

# START
for step, stp_name in enumerate(stp_names):
    print("GRAFO", step, len(stp_names), 100*(step+1)/len(stp_names), "%", f"[{stp_name}]")
    df_edges_G, terminals = read_stp("I080/"+stp_name)
    df_G, dic_incidence, dic_edges, G = pre_pros(df_edges_G)

    median_weight = df_edges_G["WEIGHT"].median()
    dic_annealing = {}
    for i, a in enumerate(gridsearch["a"]):
        for j, b in enumerate(gridsearch["b"]):
            for g in [("", False)]:
                for _, p in enumerate(["DFS"]):
                    for r in [("node", "dotted")]:
                        dic_annealing[f"{p}_{r[0]}_ixa={i}_ixb={j}"] = Annealing(
                            nf=params["nf"],
                            beta=lambda n: a * (n ** b) * (1 / median_weight),
                            df_NB_G=df_G,
                            dic_weight_edges=dic_edges,
                            terminals=terminals,
                            greedy=g[0],
                            path_approach=p,
                            remove_approach=r[0]
                        )

    root_name = "gridsearch/"+stp_name.replace(".stp", "")+"/"
    for u, (U, V) in enumerate(UNIFORMS):
        print("UNIF", u, len(UNIFORMS), 100*(u+1)/len(UNIFORMS), "%", f"[{step}]")
        for k, (key, annealing) in enumerate(dic_annealing.items()):
            print(">", key, k, len(dic_annealing), 100 * (k + 1) / len(dic_annealing), "%", f"[{u}]")
            annealing.MCMC(U, V, save_rate=params["save_rate"])
            with open(root_name+key+f"_ixu={u}_times.pickle", "wb") as f:
                pickle.dump(np.array(annealing.times), f)
            with open(root_name+key+f"_ixu={u}_CM.pickle", "wb") as f:
                pickle.dump(np.array(annealing.CM, dtype=object), f)
