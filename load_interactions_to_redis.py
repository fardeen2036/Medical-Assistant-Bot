import csv
import redis

# Connect to Redis
r = redis.Redis()

# Load from CSV
with open(r'D:\OneDrive\Desktop\new\dataset\Drug_Drug Interactions\db_drug_interactions.csv', mode='r', encoding='utf-8') as file:

    reader = csv.DictReader(file)
    for row in reader:
        drug1 = row['Drug_1'].strip().lower()
        drug2 = row['Drug_2'].strip().lower()
        interaction = row['Interaction_Description'].strip()

        # Store both directions
        key1 = f"{drug1}:{drug2}"
        key2 = f"{drug2}:{drug1}"

        r.set(key1, interaction)
        r.set(key2, interaction)

print("All interactions loaded into Redis!")
