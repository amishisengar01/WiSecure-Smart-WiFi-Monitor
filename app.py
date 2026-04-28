from flask import Flask, render_template
from live_network_scan import live_scan
import socket
import platform
packet_history = []
MAX_HISTORY = 20  # last 20 scans

app = Flask(__name__)

@app.route("/")
def scan():
    global packet_history

    scan_result = live_scan()

    # Store packet history
    packet_history.append({
        "time": scan_result["scan_timestamp"],
        "rate": scan_result["packet_rate_per_sec"]
    })

    # Keep only last N entries
    if len(packet_history) > MAX_HISTORY:
        packet_history.pop(0)

    alert = None
    if scan_result["prediction"] == "RISKY":
        alert = {
            "message": "⚠️ Suspicious network activity detected!",
            "reason": scan_result["risk_reason"],
            "time": scan_result["scan_timestamp"]
        }

    network_info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os": platform.system() + " " + platform.release()
    }

    return render_template(
        "dashboard.html",
        scan=scan_result,
        network=network_info,
        alert=alert,
        history=packet_history
    )
if __name__ == "__main__":
    app.run(debug=True)