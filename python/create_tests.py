import json
from loader import load_json
from constants import *
import random

INSTANCE_PATH = "../sujet/KIRO-large.json"


def create_json(file_path, json_content):
    with open(file_path, "w") as file:
        json.dump(json_content, file, indent=4)


instance = load_json(INSTANCE_PATH)

# 1 factory linked to every client
sol1 = empty_sol()

for site in instance[SITES]:
    sol1[PRODUCTION_CENTERS_LIST].append({ID: site[ID], AUTOMATION: 1})

for client in instance[CLIENTS]:
    sol1[CLIENTS].append({ID: client[ID], PARENT: instance[SITES][0][ID]})

sol2 = empty_sol()
l_sites = []

for site in instance[SITES]:
    sol2[PRODUCTION_CENTERS_LIST].append({ID: site[ID], AUTOMATION: 0})
    l_sites.append(site[ID])

looper = 0
for client in instance[CLIENTS]:
    sol2[CLIENTS].append({ID: client[ID], PARENT: l_sites[looper]})
    looper = (looper + 1) % len(l_sites)

sol3 = empty_sol()
l_sites_p = []
l_sites = []

for site in instance[SITES][: len(instance[SITES]) // 2]:
    sol3[PRODUCTION_CENTERS_LIST].append({ID: site[ID], AUTOMATION: 0})
    l_sites.append(site[ID])
    l_sites_p.append(site[ID])

looper = 0
for site in instance[SITES][len(instance[SITES]) // 2 :]:
    sol3[DISTRIBUTION_CENTERS_LIST].append({ID: site[ID], PARENT: l_sites_p[looper]})
    l_sites.append(site[ID])
    looper = (looper + 1) % len(l_sites_p)

looper = 0
for client in instance[CLIENTS]:
    sol3[CLIENTS].append({ID: client[ID], PARENT: l_sites[looper]})
    looper = (looper + 1) % len(l_sites)


def create_random_sol(instance):
    sol = empty_sol()
    l_sites_p = []
    l_free_sites = []
    l_taken_sites = []

    for site in instance[SITES]:
        l_free_sites.append(site[ID])

    for i in range(random.randint(1, len(l_free_sites))):
        site_chosen = random.choice(l_free_sites)
        sol[PRODUCTION_CENTERS_LIST].append(
            {ID: site_chosen, AUTOMATION: random.choice([0, 1])}
        )
        l_taken_sites.append(site_chosen)
        l_free_sites.remove(site_chosen)
        l_sites_p.append(site_chosen)

    if len(l_free_sites) > 0:
        for i in range(random.randint(0, len(l_free_sites))):
            site_chosen = random.choice(l_free_sites)
            parent_chosen = random.choice(l_sites_p)
            sol[DISTRIBUTION_CENTERS_LIST].append(
                {ID: site_chosen, PARENT: parent_chosen}
            )
            l_free_sites.remove(site_chosen)
            l_taken_sites.append(site_chosen)

    for client in instance[CLIENTS]:
        parent_chosen = random.choice(l_taken_sites)
        sol[CLIENTS].append({ID: client[ID], PARENT: parent_chosen})

    return sol


create_json("Tests/test1.json", sol1)
create_json("Tests/test2.json", sol2)
create_json("Tests/test3.json", sol3)

for i in range(4, 100):
    create_json(f"Tests/test{i}.json", create_random_sol(instance))
