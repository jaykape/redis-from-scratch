from kill_process import kill_process_on_port
import os
import signal
import socket
import subprocess
import time
import redis

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


# Test database selection
r.set("foo", "bar")
check("GET foo in db 0", r.get("foo"), "bar")
r.execute_command("SELECT", 1)
check("GET foo in db 1 (should be None)", r.get("foo"), None)
r.set("foo", "baz")
check("GET foo in db 1", r.get("foo"), "baz")
r.execute_command("SELECT", 0)
check("GET foo in db 0 (should be bar)", r.get("foo"), "bar")

print(f"\n{passed + failed} tests: {passed} passed, {failed} failed.")

# Stop the server
server_proc.terminate()
server_proc.wait()
