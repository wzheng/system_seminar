# Redis demo

## Installation on ec2
1. Get the latest version of redis
`wget http://download.redis.io/releases/redis-3.2.1.tar.gz`
2. `tar xvf redis-3.2.1.tar.gz`
3. `cd redis-3.2.1`
4. `cd deps`
5. `make hiredis jemalloc linenoise lua geohash-int`
6. `cd ..; make`
7. Start server
`./src/redis-server`
8. Start client
`./src/redis-cli`
9. Key-value operations:
`SET key1 1`
`INCR key1`
`GET key1`
10. List operation:
RPUSH mylist a
LPUSH mylist b
LRANGE mylist 0 1
11. Transaction:
MULTI
INCR key1
LPUSH mylist b
EXEC


