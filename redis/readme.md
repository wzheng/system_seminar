# Redis demo

## Single machine installation
1. Get the latest version of redis
`wget http://download.redis.io/releases/redis-3.2.1.tar.gz`
2. `tar xvf redis-3.2.1.tar.gz`
3. `cd redis-3.2.1`
4. `cd deps`
5. `make hiredis jemalloc linenoise lua geohash-int`
6. `cd ..; make`
7. Start server: `./src/redis-server`
8. Start client: `./src/redis-cli`

## Key-value store operations
1. Key-value operations
<pre>
SET key1 1
INCR key1
GET key1
</pre>
2. List operation
<pre>
RPUSH mylist a
LPUSH mylist b
LRANGE mylist 0 1
</pre>
3. Redis "transaction"
<pre>
MULTI
INCR key1
LPUSH mylist b
EXEC
</pre>

## Pub/sub operations
1. Start two clients
2. Subscribe to two channels on one client: <code>SUBSCRIBE channel1 channel2</code>
3. Publish on another client: <code>PUBLISH channel1 "hello world"</code>


## Cluster installation on ec2
1. Follow single machine installation
2. Create a new directory for each instance of redis server. Copy over the redis server from redis-3.2.1/src/redis-server to this new directory.
3. Create a new config file redis.conf
<pre>
bind IP_ADDR
port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
</pre>

Remember to open the port, and 10000 + port in the ec2 security group setting. 10000 + port is used for cluster instances to communicate with one another.

4. Install redis gem: <code>gem install redis</code>

5. Create your new cluster using the script under ./src: <code>./src/redis-trib.rb create --replicas 1 HOST1:PORT1 HOST2:PORT2 ...</code>

## Try out the redis benchmark
1. Create a new file client/redisconfig.py
2. Specify the hosts: `hosts=[{"host": 127.0.0.1, "port": 7000}, ...]`
3. Run the benchmark: `python benchmark.py --num-clients 50 --num-seconds 10 --num-channels 10 --message-size 20`