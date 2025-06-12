"""Headless daemon: listens to DHT_TOPIC, decides ON/OFF, publishes to RELAY_TOPIC.

🔹 Publishes JSON `{"type":"set_state","value":0|1}` understood by RelayWindow.
🔹 Prints every decision + uses `on_log` so you see **Sending PUBLISH …** בלייב.
🔹 Works on the same broker settings (WS :8000). Add `tls_set()` if you switch to 8884.
"""
import json, uuid, random
import paho.mqtt.client as mqtt
from ..core import config

print(config.BROKER_IP, config.BROKER_PORT)

cid = f"relay-ctl-{uuid.uuid4()}-{random.randrange(1,1_000_000):06d}"
cli = mqtt.Client(client_id=cid, transport="websockets")
cli.tls_set()

cli.username_pw_set(config.USERNAME, config.PASSWORD)

# full MQTT log – helps debug why a publish might not happen
cli.on_log = lambda c, u, l, b: print("MQTT-CTL:", b.decode() if isinstance(b, bytes) else b)

# business logic

def on_msg(_c, _u, msg):
    print("[controller] got", msg.payload)              # DEBUG
    try:
        data = json.loads(msg.payload.decode())
        temp = data.get("temperature")
    except (json.JSONDecodeError, AttributeError):
        return

    if temp is None:
        return

    on = temp > config.CLIENT_TRH
    cmd = json.dumps({"type": "set_state", "value": 1 if on else 0})
    print("⟶ publish relay", cmd)                        # DEBUG
    cli.publish(config.RELAY_TOPIC, cmd)

cli.on_message = on_msg
cli.connect(config.BROKER_IP, config.BROKER_PORT)        # 8000/ws by default
cli.subscribe(config.DHT_TOPIC)
cli.loop_forever()