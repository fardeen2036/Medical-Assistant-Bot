import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.sadd("drug:acetaminophen:interactions", "ibuprofen|Avoid combining due to increased risk of liver toxicity")
r.sadd("drug:aspirin:interactions", "ibuprofen|May reduce aspirin's effectiveness")
