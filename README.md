<p>
<picture>
<img src="/public/logo.png">
</picture>
</p>

I built a Redis implementation in Python for fun. It works almost like the real Redis you can connect using redis-cli or a Redis client from any language, most functionality is implemented.

## How to Run

Start by `cd` to the root of this repo.

### With Docker

```bash
docker build -t kape-redis .
docker run -p 6379:6379 kape-redis
```

Now your Redis server is accessible on `localhost:6379`

Or run it directly without Docker (Python >= 3.10 required)

#### Windows

```
python -m app.main
```

#### Linux/macOS

```
python3 -m app.main
```

### With a redis.conf-style file

You can now boot with a config file either as the first argument or via `--config`.

```bash
python -m app.main redis.conf
python -m app.main --config redis.conf --port 6380
```

Supported startup options currently include `bind`, `port`, `databases`, `appendonly`, `appendfilename`, `dir`, `replicaof`, `cluster-enabled`, `cluster-config-file`, `cluster-node-timeout`, `cluster-announce-ip`, `cluster-announce-port`, and `cluster-announce-bus-port`.

### Cluster bootstrap shape

The current cluster implementation now speaks the Redis cluster-bus wire protocol (header + gossip + FAIL + UPDATE frames, byte-compatible with upstream `src/cluster.h`), so nodes can discover each other at runtime rather than relying only on a pre-seeded `nodes.conf`.

- topology is loaded from each node's `cluster-config-file` using a Redis-like `nodes.conf` text format, and is updated in place as peers are discovered
- key routing uses Redis-compatible CRC16 hash slots and returns `MOVED` for the wrong primary
- replicas stream writes asynchronously from their configured master
- replica reads follow Redis Cluster semantics: clients must send `READONLY` before reading from a replica, and can switch back with `READWRITE`
- `CLUSTER MEET host port [bus-port]` opens a real outbound link on the bus port and completes the handshake with `MEET` → `PONG`
- a heartbeat cron sends `PING` every second with a gossip section of up to 3 peers, and marks peers whose last `PONG` is older than `cluster-node-timeout` as disconnected
- supported cluster admin commands now include `CLUSTER INFO`, `MYID`, `MYSHARDID`, `NODES`, `SLOTS`, `SHARDS`, `REPLICAS`, `KEYSLOT`, `COUNTKEYSINSLOT`, `GETKEYSINSLOT`, `COUNT-FAILURE-REPORTS`, `LINKS`, `SLOT-STATS`, `ADDSLOTS`/`RANGE`, `DELSLOTS`/`RANGE`, `FLUSHSLOTS`, `SETSLOT`, `MEET`, `FORGET`, `RESET`, `REPLICATE`, `FAILOVER TAKEOVER`, `BUMPEPOCH`, `SET-CONFIG-EPOCH`, `MIGRATION STATUS/LIST`, and `SAVECONFIG`

There are two end-to-end tests: `test/test_cluster_bootstrap.py` brings up a pre-seeded 9-node layout, and `test/test_cluster_meet.py` boots three fresh nodes that only know themselves and verifies they form a full mesh by `CLUSTER MEET` + gossip.
