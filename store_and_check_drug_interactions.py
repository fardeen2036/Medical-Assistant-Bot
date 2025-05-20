# 📦 Imports
import redis
import pandas as pd

# 🔗 Connect to Redis
redis_client = redis.Redis(
    host="redis-16019.c330.asia-south1-1.gce.redns.redis-cloud.com",
    port=16019,
    password="Fg49tr0oXsC9KRLawZ9nryZleACcjey2",
    decode_responses=True,
    socket_timeout=5
)

# ✅ Test Redis connection
if redis_client.ping():
    print("✅ Connected to Redis!")

# 📄 Load and clean the dataset
file_path = r"D:\OneDrive\Desktop\new\dataset\Drug_Drug Interactions\db_drug_interactions.csv"
df = pd.read_csv(file_path)
df.dropna(subset=["Drug_1", "Drug_2", "Interaction Description"], inplace=True)
print(df.head(10))

# 🧠 Store drug interactions in Redis
for _, row in df.iterrows():
    drug1 = row["Drug_1"].lower().strip()
    drug2 = row["Drug_2"].lower().strip()
    interaction_desc = row["Interaction Description"].strip()

    # Store bidirectional interactions
    redis_client.sadd(f"drug:{drug1}:interactions", f"{drug2}|{interaction_desc}")
    redis_client.sadd(f"drug:{drug2}:interactions", f"{drug1}|{interaction_desc}")

print("✅ Drug interactions stored in Redis.")

# 🔍 Function to check drug interactions
def check_drug_interaction(drug_name):
    drug_name = drug_name.lower().strip()
    interactions = redis_client.smembers(f"drug:{drug_name}:interactions")

    if not interactions:
        return f"❌ No known interactions for {drug_name}."

    print(f"⚠️ Drug interactions for {drug_name}:")
    for interaction in interactions:
        drug, desc = interaction.split("|", 1)
        print(f"   🚨 {drug}: {desc}")

# 🧪 Test the function
check_drug_interaction("Trioxsalen")

# 🔁 Test Redis read/write
redis_client.set("test_key", "hello redis!")
print(redis_client.get("test_key"))
