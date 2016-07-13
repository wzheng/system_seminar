# Redis demo

## Single machine installation
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

## Key-value store operations
1. Key-value operations
`SET key1 1
INCR key1
GET key1`
2. List operation
`RPUSH mylist a
LPUSH mylist b
LRANGE mylist 0 1`
3. Redis "transaction"
`MULTI
INCR key1
LPUSH mylist b
EXEC`

## Pub/sub operations
1. Start two clients
2. Subscribe to two channels on one client
`SUBSCRIBE channel1 channel2`
3. Publish on another client
`PUBLISH channel1 "hello world"`


## Cluster installation on ec2
1. Follow single machine installation
2. Create a new directory for each instance of redis server. Copy over the redis server from redis-3.2.1/src/redis-server to this new directory.
3. Create a new config file redis.conf
`
bind IP_ADDR
port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
`
4. Install redis gem
`gem install redis`
5. Create your new cluster with the script under ./src
`./src/redis-trib.rb create --replicas 1 HOST1:PORT1 HOST2:PORT2 ...`