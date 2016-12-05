import redis

def wipe():
    r = redis.StrictRedis(host="crawler-pr.kdoxgp.0001.use1.cache.amazonaws.com", port=6379, db=0)
    print "fin", r.flushall()

if __name__ == "__main__":
    wipe()
