import redis
from config import REDIS_INFO

pool = redis.ConnectionPool(host=REDIS_INFO[0], password=REDIS_INFO[1], port=REDIS_INFO[2], db=REDIS_INFO[3],
                            max_connections=10)

Redis = redis.StrictRedis(connection_pool=pool, decode_responses=True)

PREFIX = 'xxx:'
