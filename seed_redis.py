import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("aspirin:ibuprofen", "Increased risk of bleeding when taken together.")
r.set("paracetamol:ibuprofen", "Generally safe when taken together.")
r.set("amoxicillin:metronidazole", "May cause nausea or gastrointestinal issues.")
r.set("atorvastatin:grapefruit", "Grapefruit may increase the risk of side effects from atorvastatin.")

print("Drug interactions seeded in Redis.")
