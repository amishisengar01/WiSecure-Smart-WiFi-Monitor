import time
from scapy.all import sniff
import pandas as pd
import joblib

# Load trained ML model
model = joblib.load("network_model.pkl")

# -----------------------------
# Baseline learning (global)
# -----------------------------
BASELINE_PACKET_RATE = 0
BASELINE_SAMPLES = 0


def live_scan():
    global BASELINE_PACKET_RATE, BASELINE_SAMPLES

    packet_count = 0
    total_packet_length = 0
    fwd_packets = 0
    bwd_packets = 0
    destination_ports = []

    start_time = time.time()

    def packet_handler(packet):
        nonlocal packet_count, total_packet_length, fwd_packets, bwd_packets
        if packet.haslayer("IP"):
            packet_count += 1
            total_packet_length += len(packet)

            if packet.haslayer("TCP") or packet.haslayer("UDP"):
                fwd_packets += 1
                destination_ports.append(packet.dport)
            else:
                bwd_packets += 1

    print("📡 Capturing network traffic for 10 seconds...")
    sniff(prn=packet_handler, timeout=10)

    end_time = time.time()
    flow_duration = int((end_time - start_time) * 1000)

    packet_rate = packet_count / 10 if packet_count else 0
    avg_packet_size = total_packet_length / packet_count if packet_count else 0
    destination_port = (
        max(destination_ports, key=destination_ports.count)
        if destination_ports else 0
    )
    forward_ratio = round(fwd_packets / packet_count, 2) if packet_count else 0

    # -----------------------------
    # Baseline learning phase
    # -----------------------------
    if BASELINE_SAMPLES < 5:
        BASELINE_PACKET_RATE += packet_rate
        BASELINE_SAMPLES += 1

    avg_baseline = (
        BASELINE_PACKET_RATE / BASELINE_SAMPLES
        if BASELINE_SAMPLES else packet_rate
    )

    # -----------------------------
    # Prepare ML input
    # -----------------------------
    sample = pd.DataFrame([{
        "Destination Port": destination_port,
        "Flow Duration": flow_duration,
        "Total Fwd Packets": fwd_packets,
        "Total Backward Packets": bwd_packets,
        "Packet Length Mean": avg_packet_size
    }])

    sample = sample[model.feature_names_in_]
    ml_prediction = model.predict(sample)[0]

    # -----------------------------
    # Heuristic + Baseline logic
    # -----------------------------
    suspicious = False
    reason = "Traffic within normal operating range"

    # Spike compared to baseline
    if avg_baseline > 0 and packet_rate > avg_baseline * 3:
        suspicious = True
        reason = "Sudden spike compared to baseline traffic"

    # Extreme burst
    if packet_count > 50000 and flow_duration < 10000:
        suspicious = True
        reason = "High-volume burst in short duration"

    # Unusual port under load
    if destination_port not in [80, 443, 53] and packet_rate > avg_baseline * 2:
        suspicious = True
        reason = "High traffic on uncommon destination port"

    # Final decision
    prediction = 1 if suspicious else ml_prediction

    # -----------------------------
    # Risk scoring
    # -----------------------------
    if prediction == 0:
        risk_score = min(30, int((packet_rate / (avg_baseline + 1)) * 10))
        threat_level = "Low"
        status = "SAFE"
    else:
        risk_score = min(100, 70 + int((packet_rate / (avg_baseline + 1)) * 15))
        threat_level = "High"
        status = "RISKY"

    # -----------------------------
    # Result
    # -----------------------------
    return {
        "scan_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "packets_captured": packet_count,
        "packet_rate_per_sec": round(packet_rate, 2),
        "avg_packet_size": round(avg_packet_size, 2),
        "dominant_destination_port": destination_port,
        "forward_packet_ratio": forward_ratio,
        "baseline_packet_rate": round(avg_baseline, 2),
        "prediction": status,
        "risk_score": risk_score,
        "threat_level": threat_level,
        "risk_reason": reason
    }