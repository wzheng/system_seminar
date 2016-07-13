# ZooKeeper

1. Get the latest version of ZooKeeper: `wget http://ftp.wayne.edu/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz`
2. `tar xvf http://ftp.wayne.edu/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz`
3. Create configuration file in conf/zoo.cfg
<pre>
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
</pre>
4. Start server: `bin/zkServer.sh start`
5. Start client: `bin/zkCli.sh -server 127.0.0.1:2181`
6. Show the list of znodes: `ls /`
7. Create a new znode: `create /key1 value1`
8. Get znode: `get /key1`
9. Set this znode to a new value: `set /key1 value2`
10. Set a watch on this znode: `get /key1 true`

To set up replication on different nodes, simply change the configuration file:
<pre>
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
server.1=zoo1:2888:3888
server.2=zoo2:2888:3888
server.3=zoo3:2888:3888
</pre>

Each machine should have the same configuration file.

## ZooKeeper benchmark
Run the zookeeper smoke test from here: https://github.com/phunt/zk-smoketest