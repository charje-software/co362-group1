import time

from oracle import Oracle

oracle = Oracle()

while True:
    try:
        oracle.update_consumption()
    except Exception:
        print("All oracle data consumed. Stopping oracle...")
        break
    time.sleep(15)
