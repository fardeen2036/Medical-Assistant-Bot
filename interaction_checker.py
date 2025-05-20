import redis

r = redis.Redis()

def check_interactions(drug_list):
    interactions = []
    for i in range(len(drug_list)):
        for j in range(i + 1, len(drug_list)):
            key1 = f"{drug_list[i].lower()}:{drug_list[j].lower()}"
            key2 = f"{drug_list[j].lower()}:{drug_list[i].lower()}"
            interaction = r.get(key1) or r.get(key2)
            if interaction:
                interactions.append((drug_list[i], drug_list[j], interaction.decode()))
    return interactions
