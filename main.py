def check_drug_interaction(drug1, drug2):
    key = f"{drug1}:{drug2}"

    # Check if interaction exists in cache
    cached_result = redis_client.get(key)
    if cached_result:
        return f"(From Redis Cache) {cached_result}"

    # Else: Check from DataFrame
    interaction = df[
        ((df['Drug_1'] == drug1) & (df['Drug_2'] == drug2)) |
        ((df['Drug_1'] == drug2) & (df['Drug_2'] == drug1))
    ]

    if not interaction.empty:
        result = interaction['Interaction Description'].values[0]
        redis_client.set(key, result)  # Save to Redis
        return f"(From DB) {result}"
    else:
        redis_client.set(key, "No interaction found.")
        return "No interaction found."
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import redis

app = FastAPI()

# Allow requests from your frontend (React on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.post("/check-interaction")
async def check_interaction(data: dict = Body(...)):
    drug1 = data.get("drug1", "").lower()
    drug2 = data.get("drug2", "").lower()
    key1 = f"{drug1}:{drug2}"
    key2 = f"{drug2}:{drug1}"

    interaction = redis_client.get(key1) or redis_client.get(key2)
    if interaction:
        return {"message": f"Interaction found: {interaction}"}
    return {"message": "No known interaction."}
