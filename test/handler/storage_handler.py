from services import CFG_OBJ
from redis import StrictRedis, ConnectionPool

class RedisAdapter():
    def __init__(self):
        redis_conn_pool = ConnectionPool(
            host=CFG_OBJ.get('STORAGE.REDIS.HOST'),
            port=CFG_OBJ.get('STORAGE.REDIS.PORT'),
            db=0
        )
        self._redis_instance = StrictRedis(connection_pool=redis_conn_pool)

    def get_instance(self):
        return self._redis_instance
