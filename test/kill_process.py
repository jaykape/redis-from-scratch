import os
import signal
import socket
import subprocess
import time


def kill_process_on_port(port=6379):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("localhost", port))
            s.close()
    except OSError:
        # Port is in use, try to kill the process using netstat and taskkill (Windows)
        try:
            result = subprocess.check_output(
                f'netstat -ano | findstr :{port}', shell=True, text=True)
            for line in result.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        os.system(f'taskkill /PID {pid} /F')
                        time.sleep(1)
        except Exception as e:
            print(f"Could not kill process on port {port}: {e}")
