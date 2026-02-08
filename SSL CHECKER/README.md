#  SSL Certificate Checker

A secure and user-friendly Flask web application that allows users to check SSL/TLS certificate details for any website domain.

## Features

- **Domain SSL Check**: Enter any domain to retrieve its SSL certificate details
- **Certificate Information Display**:
  - Issued To (Common Name)
  - Issued By (Certificate Authority)
  - Valid From & Valid Till dates
  - Days remaining before expiry
- **Status Indicators**: Visual green (VALID) / red (EXPIRED) status badges
- **Error Handling**: Graceful handling of invalid domains, timeouts, and SSL errors
- **Modern UI**: Clean, responsive design with animations

## Technologies Used

| Technology | Purpose |

| **Python 3** => Backend programming language 
| **Flask** => Web framework for routing and templating 
| **ssl** => SSL/TLS connection and certificate handling 
| **socket** => Network socket connections 
| **datetime** => Date parsing and expiry calculations 
| **HTML/CSS** => Frontend user interface 



## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps


1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open in browser**:
   ```
   http://127.0.0.1:5000
   ```

## How It Works


### Key Concepts (For Viva/Interviews)

#### 1. SSL/TLS Handshake
When a client connects to a server over HTTPS:
1. Client sends "Hello" with supported cipher suites
2. Server responds with chosen cipher and its certificate
3. Client verifies certificate with trusted Certificate Authorities
4. Secure encrypted channel is established

#### 2. X.509 Certificates
- Standard format for public key certificates
- Contains: Subject (who), Issuer (CA), Validity dates, Public key
- Signed by Certificate Authority to prove authenticity

#### 3. Python ssl Module
```python
# Create secure context with default settings
context = ssl.create_default_context()

# Wrap socket with SSL, enabling SNI
with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
    cert = ssl_sock.getpeercert()  # Get certificate as dictionary
```

#### 4. Flask Request Handling
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain')
        # Process and return results
    return render_template('index.html')
```

##  Sample Output

### Valid Certificate
```
Certificate is VALID

Domain:         google.com
Issued To:      *.google.com
Issued By:      GTS CA 1C3
Valid From:     2024-01-15 08:00:00
Valid Till:     2024-04-08 08:00:00
Days Remaining: 84 days
```

### Error Response
```
Error
Invalid domain: notarealdomainxyz123.com could not be resolved
```

## Error Handling

| Error Type , Description 

| `socket.timeout` => Connection took too long (>10 seconds) 
| `socket.gaierror` => Domain name doesn't exist 
| `SSLCertVerificationError` => Invalid/untrusted certificate 
| `ConnectionRefusedError` => Server not accepting HTTPS 

## Future Enhancements

- [ ] Multiple domain checking
- [ ] SSL expiry email alerts
- [ ] Export report as PDF/CSV
- [ ] Certificate chain visualization
- [ ] Cloud deployment (Render/Railway)

## Interview Talking Points

1. **Why use `ssl.create_default_context()`?**
   - Automatically loads system CA certificates
   - Uses secure TLS versions (1.2+)
   - Enables hostname verification

2. **What is SNI (Server Name Indication)?**
   - TLS extension allowing multiple SSL sites on one IP
   - Client specifies which hostname it's connecting to

3. **Why port 443?**
   - Standard port for HTTPS traffic
   - Firewalls typically allow this port

4. **Security considerations?**
   - Never disable certificate verification in production
   - Set timeouts to prevent DoS vulnerabilities
   - Validate and sanitize user input

## License

This project is open source and available for educational purposes.

---


