# Prerequisites

## mongodb download and install
    https://www.mongodb.com/try/download/community

## mongodb shell download and install
    https://www.mongodb.com/try/download/shell

## mongo compass download and install
    https://www.filehorse.com/download-mongodb-compass/


# For first run, create some empty folders in C:/data.

# mongodb sharding

# Sharding setup (localhost):

## Define config server
    Config server:
        mongod --configsvr --port 28041 --replSet config_repl --dbpath C:\data\configsrv1 --bind_ip localhost

        mongod --configsvr --port 28042 --replSet config_repl --dbpath C:\data\configsrv2 --bind_ip localhost

        mongod --configsvr --port 28043 --replSet config_repl --dbpath C:\data\configsrv3 --bind_ip localhost

        mongosh --host localhost  --port 28041

        rsconf = {
            _id: "config_repl",
            members: [
                {
                    _id: 0,
                    host: "localhost:28041",
                },
                {   _id: 1,
                    host: "localhost:28042",
                },
                {
                    _id: 2,
                    host: "localhost:28043"
                }
            ]
        }

        rs.initiate(rsconf)
        rs.status()

## First shard with 3 replicas
    Shard server:
        mongod --shardsvr --port 28081 --replSet shard_repl --dbpath C:\data\shardrep1 --bind_ip localhost

        mongod --shardsvr --port 28082 --replSet shard_repl --dbpath C:\data\shardrep2 --bind_ip localhost

        mongod --shardsvr --port 28083 --replSet shard_repl --dbpath C:\data\shardrep3 --bind_ip localhost

        mongosh --host localhost  --port 28081

        rsconf = {
            _id: "shard_repl",
            members: [
                {
                    _id: 0,
                    host: "localhost:28081",
                },
                {   _id: 1,
                    host: "localhost:28082",
                },
                {
                    _id: 2,
                    host: "localhost:28083"
                }
            ]
        }

        rs.initiate(rsconf)
        rs.status()

## Second shard with 3 replicas
        mongod --shardsvr --port 29081 --replSet shard2_repl --dbpath C:\data\shard2rep1 --bind_ip localhost

        mongod --shardsvr --port 29082 --replSet shard2_repl --dbpath C:\data\shard2rep2 --bind_ip localhost

        mongod --shardsvr --port 29083 --replSet shard2_repl --dbpath C:\data\shard2rep3 --bind_ip localhost

        mongosh --host localhost  --port 29081

        rsconf = {
            _id: "shard2_repl",
            members: [
                {
                    _id: 0,
                    host: "localhost:29081",
                },
                {   _id: 1,
                    host: "localhost:29082",
                },
                {
                    _id: 2,
                    host: "localhost:29083"
                }
            ]
        }

        rs.initiate(rsconf)
        rs.status()

## Third shard with 3 replicas
        mongod --shardsvr --port 29071 --replSet shard3_repl --dbpath C:\data\shard3rep1 --bind_ip localhost

        mongod --shardsvr --port 29072 --replSet shard3_repl --dbpath C:\data\shard3rep2 --bind_ip localhost

        mongod --shardsvr --port 29073 --replSet shard3_repl --dbpath C:\data\shard3rep3 --bind_ip localhost

        mongosh --host localhost  --port 29071

        rsconf = {
            _id: "shard3_repl",
            members: [
                {
                    _id: 0,
                    host: "localhost:29071",
                },
                {   _id: 1,
                    host: "localhost:29072",
                },
                {
                    _id: 2,
                    host: "localhost:29073"
                }
            ]
        }

        rs.initiate(rsconf)
        rs.status()

# Create Mongo server
    MongoS:
        mongos --port 35000 --configdb config_repl/localhost:28041,localhost:28042,localhost:28043 --bind_ip localhost 

## Connect to the Sharded Cluster
        mongosh --host localhost --port 35000

        sh.addShard("shard_repl/localhost:28081,localhost:28082,localhost:28083")
        sh.addShard("shard2_repl/localhost:29081,localhost:29082,localhost:29083")
        sh.addShard("shard3_repl/localhost:29071,localhost:29072,localhost:29073")

### enable sharding for "benchmark" database
        sh.enableSharding("benchmark")

        sh.status()
        use benchmark
### create collections in "benchmark" (collections are tables in DB)
        db.createCollection('testindexing')
        db.createCollection('testview')
        db.createCollection('testshard')

### define indexing for "testindexing" collection
        db.testshard.createIndex({"number": "hashed" })

### define sharding by "number" field
        sh.shardCollection("benchmark.testshard", {"number": "hashed" })

        db.testshard.getShardDistribution()

### mongodb indexing by "number" field
    db.testindexing.createIndex({"number": 1 })

# mongodb view
    db.createView(
        "viewTest",
        "testview",
        [{ $project: { "number": 1, id: "$id", name: "$name", date: "$date", result: "$result" } }]
    )

# At first run, create benchmark database in mongo compass and import test.json file into testview, testshard, testindexing collection.

# flask run 
`pip install -r requirements.txt'


flask --app app.py --debug run 