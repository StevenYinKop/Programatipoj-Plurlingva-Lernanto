# Superlift Garage Door Remote Control via AWS IoT + ESP32

## 1. Overview
This document describes how to build a secure remote control system for a **Superlift RDO-6 roller door** using **ESP32 + AWS IoT Core + AWS Lambda + API Gateway**.

### Goal
- Remotely toggle your Superlift garage door (no state feedback required).
- Control from any smartphone or CarPlay via HTTPS → AWS Lambda → AWS IoT → ESP32.
- Ensure security via AWS IAM and HTTPS authentication.

### System Architecture
```
[Mobile App / Shortcut / CarPlay]
        │ HTTPS Request (secured via API Key / HMAC)
        ▼
[AWS API Gateway] ───► [AWS Lambda: garage-door-trigger]
                             │
                             ▼ MQTT Publish
                     [AWS IoT Core: Topic garage/door/control]
                             │
                             ▼
                      [ESP32 + Relay Module]
                             │
                             ▼
                  [Superlift RDO-6 PB Interface]
```

---

## 2. Bill of Materials (BOM)

| Item | Recommended Model | Qty | Purpose | Notes |
|------|--------------------|------|----------|--------|
| ESP32 Dev Board | ESP32-DevKitC / NodeMCU-ESP32 | 1 | Main microcontroller | You already have it |
| Relay Module | Single channel 5V relay (SRD-05VDC-SL-C) | 1 | Simulate button press | Prefer optocoupled module |
| Buck Converter | LM2596 DC-DC 24V→5V | 1 | Convert control box 24V to ESP32 5V | Adjustable output |
| Screw Terminal Adapter | 2P terminal to Dupont | 2 | Easy PB & power wiring | Optional |
| ABS Enclosure Box | 100x80x60 mm | 1 | Protect electronics | Mount near control box |
| Cable ties / 3M adhesive | — | — | Fix cables safely | Optional |
| Dupont wires | Male-female | Several | Wiring | Already owned |

---

## 3. Hardware Wiring (Detailed Guide)

### 3.1 Power: Connecting the Buck Converter (LM2596)
Your Superlift control box provides a 24V DC output internally (for FLASH light or accessories). The ESP32 cannot use 24V directly — it must be stepped down to 5V.

#### Step-by-Step:
1. Identify a **24V DC output** inside or near your Superlift control box (commonly labeled “FLASH 24V”).
2. Connect those two wires to the **input terminals** of the LM2596 module:
   - **IN+ → +24V (red wire)**
   - **IN− → GND (black wire)**
3. Use a multimeter to adjust the LM2596’s small screw until the **output measures 5.0V**.
4. Connect the LM2596 **output terminals** to the ESP32:
   - **OUT+ → ESP32 VIN (or 5V pin)**
   - **OUT− → ESP32 GND**

> ⚠️ Important: Always share the same ground between LM2596, ESP32, and Relay. Without common ground, the relay will not trigger correctly.

#### Wiring diagram:
```
24V (Superlift) ──► [IN+] LM2596 [OUT+] ──► ESP32 5V (VIN)
GND (Superlift) ──► [IN-] LM2596 [OUT-] ──► ESP32 GND
```

### 3.2 Connecting the Relay Module
The relay module acts as a “virtual finger” to press the PB button on your Superlift controller.

#### Step-by-Step:
1. Connect the relay’s **power and control** pins:
   - **VCC → 5V (from LM2596 output or ESP32 5V pin)**
   - **GND → ESP32 GND (shared)**
   - **IN → ESP32 GPIO4** (you can change pin number in your Arduino code)

2. Connect the **relay switching contacts** (COM and NO) to the Superlift control box PB interface:
   - **COM → PB terminal 1**
   - **NO → PB terminal 2**

When GPIO4 outputs HIGH for ~0.5 seconds, the relay closes COM–NO, shorting the PB contacts, just like pressing the wall button.

#### Wiring diagram:
```
ESP32 GPIO4 ───► Relay IN
ESP32 5V ─────► Relay VCC
ESP32 GND ────► Relay GND

Relay COM ─────► PB terminal 1
Relay NO  ─────► PB terminal 2
```

> 💡 Tip: The relay’s onboard LED will blink when activated. You should also hear a distinct “click”.

### 3.3 Combined Wiring Layout
```
       +---------------------+      +----------------+      +-----------------+
       | Superlift Control   |      | LM2596 Buck    |      | ESP32 + Relay   |
       | Box (PB + 24V out)  |      | Converter      |      | Control Module  |
       |                     |      | 24V→5V Output  |      |                 |
       |   PB1◄──────────────┼──────┤                │      |  GPIO4→Relay IN  |
       |   PB2◄──────────────┤      │                │      |  5V→Relay VCC   |
       |  +24V◄──────────────┤IN+   │ OUT+──────────►5V     |  GND Shared     |
       |  GND◄───────────────┤IN−   │ OUT−──────────►GND    +-----------------+
       +---------------------+      +----------------+ 
```

### 3.4 Assembly & Mounting Recommendations
- Mount LM2596, relay, and ESP32 on a **non-conductive base** (plastic board or inside ABS enclosure).
- Use **double-sided tape** or **small screws** to secure modules.
- Route cables neatly with **zip ties** or **spiral wraps**.
- Keep modules at least 5 cm away from the motor’s high-voltage section.
- Ensure all joints are insulated — use heat-shrink tubing or electrical tape.

### 3.5 Testing Sequence
1. **Bench Test First** – Power ESP32 via USB; verify relay clicks when code runs.
2. **Power Test** – Connect LM2596 and measure output is 5.0V.
3. **Integration Test** – Connect relay COM/NO to PB terminals, trigger via MQTT and verify the door responds.

---

## 4. Arduino Firmware (ESP32)

### 4.1 Libraries Required
- WiFi.h
- WiFiClientSecure.h
- PubSubClient.h (MQTT client)

### 4.2 MQTT Topics
- Subscribe: `garage/door/control`
- Expected message:
  ```json
  {"cmd": "press"}
  ```

### 4.3 Example Code
```cpp
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#define RELAY_PIN 4
#define PRESS_MS 500

// ===== WiFi Credentials =====
const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASS";

// ===== AWS IoT Settings =====
const char* MQTT_HOST = "YOUR_AWS_IOT_ENDPOINT"; // e.g. xxxx-ats.iot.ap-southeast-2.amazonaws.com
const int MQTT_PORT = 8883;
const char* MQTT_SUB_TOPIC = "garage/door/control";
const char* CLIENT_ID = "GarageDoorClient";

// Certificates
static const char CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
Your Amazon Root CA 1
-----END CERTIFICATE-----
)EOF";

static const char CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
Device certificate here
-----END CERTIFICATE-----
)KEY";

static const char CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
Device private key here
-----END RSA PRIVATE KEY-----
)KEY";

WiFiClientSecure net;
PubSubClient client(net);

void pressButton() {
  digitalWrite(RELAY_PIN, HIGH);
  delay(PRESS_MS);
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("[INFO] PB triggered");
}

void messageHandler(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.printf("[MQTT] Received: %s\n", msg.c_str());
  if (msg.indexOf("press") >= 0) pressButton();
}

void connectAWS() {
  net.setCACert(CERT_CA);
  net.setCertificate(CERT_CRT);
  net.setPrivateKey(CERT_PRIVATE);

  while (!client.connected()) {
    Serial.println("[INFO] Connecting to AWS IoT...");
    if (client.connect(CLIENT_ID)) {
      Serial.println("[INFO] Connected!");
      client.subscribe(MQTT_SUB_TOPIC);
    } else {
      Serial.print("[WARN] Failed, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[INFO] WiFi connected!");

  client.setServer(MQTT_HOST, MQTT_PORT);
  client.setCallback(messageHandler);
  connectAWS();
}

void loop() {
  if (!client.connected()) connectAWS();
  client.loop();
}
```

---

## 5. AWS Configuration

### 5.1 IoT Core Setup
1. Create a **Thing** (e.g., `GarageDoorESP32`).
2. Download the device certificate, private key, and root CA.
3. Attach an IoT Policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["iot:Connect", "iot:Publish", "iot:Subscribe", "iot:Receive"],
         "Resource": ["*"]
       }
     ]
   }
   ```
4. Note down the IoT endpoint (e.g., `xxxx-ats.iot.ap-southeast-2.amazonaws.com`).

### 5.2 Lambda Function
Create a Lambda function named **`garage-door-trigger`**:

```python
import boto3
import json
import hashlib, hmac, time, os

iot = boto3.client('iot-data', region_name='ap-southeast-2')

SECRET = os.environ['HMAC_SECRET']  # store in Lambda environment variable

# Validate request signature
def is_valid(headers):
    sig = headers.get('x-signature')
    ts = int(headers.get('x-timestamp', 0))
    now = int(time.time())
    if abs(now - ts) > 30:
        return False
    calc = hmac.new(SECRET.encode(), f"{headers.get('x-api-key','')}{ts}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(calc, sig)

def lambda_handler(event, context):
    headers = event.get('headers', {})
    if not is_valid(headers):
        return {'statusCode': 401, 'body': 'Unauthorized'}

    topic = 'garage/door/control'
    payload = json.dumps({ 'cmd': 'press' })
    iot.publish(topic=topic, qos=1, payload=payload)
    return {'statusCode': 200, 'body': json.dumps({'result': 'triggered'})}
```

### 5.3 API Gateway
1. Create a **REST API** (e.g., `GarageDoorAPI`).
2. Create a **POST** method linked to the Lambda above.
3. Enable **API Key** and create a Usage Plan (limit e.g. 1 req/sec, 50 req/day).
4. Add **WAF (Web Application Firewall)** to block non-AU IPs or frequent attacks.
5. Deploy the API and obtain the HTTPS endpoint.

### 5.4 Secure Test Command
```bash
TIMESTAMP=$(date +%s)
SIG=$(echo -n "YOUR_API_KEY${TIMESTAMP}" | openssl dgst -sha256 -hmac "YOUR_HMAC_SECRET" | cut -d" " -f2)

curl -X POST https://your-api-id.execute-api.ap-southeast-2.amazonaws.com/prod/trigger \
     -H "x-api-key: YOUR_API_KEY" \
     -H "x-timestamp: ${TIMESTAMP}" \
     -H "x-signature: ${SIG}" \
     -d '{"action":"press"}'
```
Only signed requests with valid API Key and recent timestamp will be accepted.

---

## 6. Mounting & Safety

### 6.1 Enclosure Installation
- Place ESP32 + relay + LM2596 in an **ABS insulated enclosure**.
- Mount near the Superlift control box using **3M tape** or **screws**.
- Ensure ventilation and dry environment.

### 6.2 Electrical Safety
- Only connect to **low-voltage terminals (24V & PB)**.
- Never touch 240V AC lines inside the control box.
- All grounds (ESP32, relay, LM2596) must be common.

### 6.3 Debugging
- Test with USB power first (ESP32 only) to verify relay action.
- When relay clicks and door responds, power via LM2596.

---

## 7. Security Design Details (API Gateway Hardening)

### 7.1 Security Objectives
- Prevent unauthorized users from toggling your garage door.
- Block automated abuse, replay attacks, and brute-force attempts.

### 7.2 Recommended Security Stack
| Layer | Component | Function |
|--------|------------|-----------|
| Network | HTTPS | Encrypts all traffic end-to-end |
| API | API Key | Basic access control per client |
| Header | HMAC Signature | Prevents replay and forgery |
| Throttling | Usage Plan | Rate limiting (1/sec, 50/day) |
| Perimeter | AWS WAF | Region/IP restriction, bot protection |
| Logging | CloudWatch | Track all invocations for auditing |

### 7.3 Why API Key Alone Is Not Enough
API Key protects against random calls but can be leaked. Adding **HMAC + timestamp** ensures each request is unique and short-lived (valid for 30s max).

### 7.4 API Gateway + Lambda Validation Flow
```
Client → HTTPS → API Gateway
         │
         ├─ Checks API Key validity
         │
         ├─ Lambda validates HMAC(timestamp, key)
         │
         ├─ Lambda publishes MQTT → AWS IoT
         │
         └─ ESP32 receives command securely
```

### 7.5 Additional Hardening Steps
- ✅ Use CloudWatch to monitor unusual access.
- ✅ Rotate API keys and HMAC secrets periodically.
- ✅ Block IPs outside Australia via AWS WAF.
- ✅ Disable unused HTTP methods (OPTIONS/GET).
- ✅ Apply minimum IAM permissions to Lambda (`iot:Publish` only to the target topic).

### 7.6 When to Use Cognito or IAM SigV4
For multi-user or shared household setups, integrate **AWS Cognito** for JWT-based login or **IAM SigV4** signing for advanced identity control. Both methods are stronger but require additional setup.

### 7.7 Summary of Security Model
> Recommended configuration for personal setup: **API Key + HMAC + HTTPS + WAF (AU-only)**.

This provides:
- High security (no open API)
- Simplicity (no local server)
- Minimal maintenance cost

---

## 8. Maintenance
- Check connections every 6–12 months.
- Ensure 5V output from LM2596 remains stable.
- Keep ESP32 firmware up to date.
- Rotate API Key and secret annually.

---

## 9. Summary
You now have a secure and simple AWS-connected garage door control system:
- **AWS IoT Core** handles secure communication.
- **Lambda + API Gateway** allows remote HTTPS triggers.
- **ESP32 + Relay** toggles your Superlift PB button.
- **API Key + HMAC + WAF** ensures only authorized clients can control it.

All components operate safely on low voltage, no local server required.

---

**Author:** Steven (2025)

**Version:** v1.1 (with Security Design)

