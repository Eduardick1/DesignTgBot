from DataBase import redis

l = [7,4,5,3]

# for n in l:
#     redis.sadd('todelete', n)

# for d in redis.smembers('todelete'):
    # print(d)

print(redis.spop('todelete'))
print(redis.smembers('todelete'))
if redis.scard('todelete') == 0:
    print("No values")