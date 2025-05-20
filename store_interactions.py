{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "a95bebb2-219d-4885-88b8-f99809431d64",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Connected to Redis!\n"
     ]
    }
   ],
   "source": [
    "import redis\n",
    "import pandas as pd\n",
    "import time\n",
    "\n",
    "# Connect to Redis\n",
    "redis_client = redis.Redis(\n",
    "    host=\"redis-16019.c330.asia-south1-1.gce.redns.redis-cloud.com\",\n",
    "    port=16019,\n",
    "    password=\"Fg49tr0oXsC9KRLawZ9nryZleACcjey2\",\n",
    "    decode_responses=True\n",
    ")\n",
    "\n",
    "# Test Redis connection\n",
    "if redis_client.ping():\n",
    "    print(\"✅ Connected to Redis!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "a7fde958-d9a6-4c8d-95cd-8ba42a9ec29e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🧹 Redis flushed.\n"
     ]
    }
   ],
   "source": [
    "# OPTIONAL: Flush all Redis data (use only if you want a clean slate)\n",
    "redis_client.flushall()\n",
    "print(\"🧹 Redis flushed.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "37e4015d-3964-4683-ba93-a3069e1d950d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load dataset (limit to 10,000 rows to avoid memory issues)\n",
    "file_path = r\"D:\\OneDrive\\Desktop\\new\\dataset\\Drug_Drug Interactions\\db_drug_interactions.csv\"\n",
    "df = pd.read_csv(file_path)\n",
    "\n",
    "# Rename columns to match expected ones if needed\n",
    "df.rename(columns=lambda x: x.strip(), inplace=True)\n",
    "\n",
    "# Drop rows with missing values\n",
    "df.dropna(subset=[\"Drug_1\", \"Drug_2\", \"Interaction_Description\"], inplace=True)\n",
    "\n",
    "# Limit data for memory safety\n",
    "df = df.head(10000)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "3e8f7de1-c1a3-4f88-a55a-f4e73bd5a2dc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Inserted chunk: 0 - 1000\n",
      "✅ Inserted chunk: 1000 - 2000\n",
      "✅ Inserted chunk: 2000 - 3000\n",
      "✅ Inserted chunk: 3000 - 4000\n",
      "✅ Inserted chunk: 4000 - 5000\n",
      "✅ Inserted chunk: 5000 - 6000\n",
      "✅ Inserted chunk: 6000 - 7000\n",
      "✅ Inserted chunk: 7000 - 8000\n",
      "✅ Inserted chunk: 8000 - 9000\n",
      "✅ Inserted chunk: 9000 - 10000\n",
      "✅ Drug interactions stored in Redis.\n"
     ]
    }
   ],
   "source": [
    "# Store in Redis using pipeline (efficient bulk insert)\n",
    "chunk_size = 1000\n",
    "for start in range(0, len(df), chunk_size):\n",
    "    chunk = df.iloc[start:start + chunk_size]\n",
    "    pipe = redis_client.pipeline()\n",
    "    for _, row in chunk.iterrows():\n",
    "        drug1 = row[\"Drug_1\"].strip().lower()\n",
    "        drug2 = row[\"Drug_2\"].strip().lower()\n",
    "        interaction_desc = row[\"Interaction_Description\"]\n",
    "\n",
    "        pipe.sadd(f\"drug:{drug1}:interactions\", f\"{drug2}|{interaction_desc}\")\n",
    "        pipe.sadd(f\"drug:{drug2}:interactions\", f\"{drug1}|{interaction_desc}\")\n",
    "    pipe.execute()\n",
    "    print(f\"✅ Inserted chunk: {start} - {start + chunk_size}\")\n",
    "\n",
    "print(\"✅ Drug interactions stored in Redis.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
