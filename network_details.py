import socket
import psutil
import platform
import time

def get_network_details():
    details = {}

    details["hostname"] = socket.gethostname()
    details["os"] = platform.system() + " " + platform.release()

    # Detect active IPv4 interface
    connected = False
    ip_address = None
    interfaces = []

    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if (
    addr.family == socket.AF_INET
    and not addr.address.startswith("127.")
    and not addr.address.startswith("169.254.")
):
                connected = True
                ip_address = addr.address
                interfaces.append({
                    "interface": iface,
                    "ip": addr.address
                })

    details["connected"] = connected
    details["ip_address"] = ip_address
    details["interfaces"] = interfaces

    return details