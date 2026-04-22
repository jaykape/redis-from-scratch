import redis
import time
import subprocess
import socket
import signal
import os
from kill_process import kill_process_on_port


kill_process_on_port(6379)


# Start the server
server_proc = subprocess.Popen([
    os.sys.executable, '-m', 'app.main'
])
time.sleep(2)  # Give the server time to start

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

passed = 0
failed = 0


def check(label: str, got, expected) -> None:
    global passed, failed
    if got == expected:
        print(f"  PASS  {label}: {got!r}")
        passed += 1
    else:
        print(f"  FAIL  {label}: got {got!r}, expected {expected!r}")
        failed += 1


check("PING", r.ping(), True)

r.set("name", "kapeRedis")
check("GET name", r.get("name"), "kapeRedis")

r.set("temp", "bye", ex=10)
check("GET temp", r.get("temp"), "bye")
ttl = r.ttl("temp")
check("TTL temp in range", 0 < ttl <= 10, True)

r.set("todelete", "yes")
r.delete("todelete")
check("GET todelete after DEL", r.get("todelete"), None)

r.set("exists_key", "1")
check("EXISTS exists_key", r.exists("exists_key"), 1)
check("EXISTS missing_key", r.exists("missing_key"), 0)

r.set("counter", "10")
check("INCR counter", r.incr("counter"), 11)
check("DECR counter", r.decr("counter"), 10)

r.set("foo", "1")
r.set("bar", "2")
check("KEYS foo*", r.keys("foo*"), ["foo"])

check("CONFIG GET appendonly", r.config_get(
    "appendonly"), {"appendonly": "no"})

print(f"\n{passed + failed} tests: {passed} passed, {failed} failed.")

# Stop the server
server_proc.terminate()
server_proc.wait()
