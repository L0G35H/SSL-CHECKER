
# IMPORTS
from flask import Flask, render_template, request
import ssl                  # For creating SSL context and handling certificates
import socket              # For establishing network connections
from datetime import datetime  # For date parsing and expiry calculations


# FLASK APPLICATION INITIALIZATION

app = Flask(__name__)


# SSL CERTIFICATE FETCHING FUNCTION

def get_ssl_certificate_info(domain: str) -> dict:
    
    # Remove common prefixes if user accidentally includes them
    # This makes the application more user-friendly
    domain = domain.strip()
    domain = domain.replace('https://', '').replace('http://', '')
    domain = domain.rstrip('/')
    
    # Validate that domain is not empty
    if not domain:
        return {'error': 'Please enter a valid domain name'}
    
    try:
        
        # STEP 1: Create SSL Context
        
        # ssl.create_default_context() creates a new SSLContext object
        # with secure default settings. It automatically:
        # - Loads system CA certificates for verification
        # - Sets secure protocol versions (TLS 1.2+)
        # - Enables certificate verification
       
        context = ssl.create_default_context()
        
        
        # STEP 2: Create Socket Connection
        
        # socket.create_connection() establishes a TCP connection
        # - Port 443 is the standard HTTPS port
        # - Timeout of 10 seconds prevents hanging on slow servers
        
        with socket.create_connection((domain, 443), timeout=10) as sock:
            
            
            # STEP 3: Wrap Socket with SSL/TLS
            
            # context.wrap_socket() performs the SSL/TLS handshake
            # - server_hostname enables SNI (Server Name Indication)
            # - SNI allows multiple SSL sites on one IP address
            
            with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
                
                
                # STEP 4: Retrieve X.509 Certificate
                
                # getpeercert() returns the certificate as a dictionary
                # X.509 is the standard format for public key certificates
                
                cert = ssl_sock.getpeercert()
                
                
                # STEP 5: Parse Certificate Fields
                
                
                # Extract 'Issued To' (Common Name - CN)
                # The subject field contains identity information
                subject = dict(item[0] for item in cert['subject'])
                issued_to = subject.get('commonName', 'N/A')
                
                # Extract 'Issued By' (Certificate Authority)
                # The issuer field identifies who signed the certificate
                issuer = dict(item[0] for item in cert['issuer'])
                issued_by = issuer.get('organizationName', issuer.get('commonName', 'N/A'))
                
                # Parse validity dates
                # Certificate dates are in format: 'Mon DD HH:MM:SS YYYY GMT'
                date_format = '%b %d %H:%M:%S %Y %Z'
                
                valid_from_str = cert['notBefore']
                valid_to_str = cert['notAfter']
                
                valid_from = datetime.strptime(valid_from_str, date_format)
                valid_to = datetime.strptime(valid_to_str, date_format)
                
                
                # STEP 6: Calculate Days Remaining
                
                # Compare expiry date with current date
                today = datetime.utcnow()
                days_remaining = (valid_to - today).days
                
                
                # STEP 7: Determine Certificate Status
                
                if days_remaining > 0:
                    status = 'VALID'
                    status_class = 'valid'  # CSS class for green styling
                else:
                    status = 'EXPIRED'
                    status_class = 'expired'  # CSS class for red styling
                
                # Return all certificate information as a dictionary
                return {
                    'domain': domain,
                    'issued_to': issued_to,
                    'issued_by': issued_by,
                    'valid_from': valid_from.strftime('%Y-%m-%d %H:%M:%S'),
                    'valid_to': valid_to.strftime('%Y-%m-%d %H:%M:%S'),
                    'days_remaining': days_remaining,
                    'status': status,
                    'status_class': status_class,
                    'error': None
                }
                
    
    # ERROR HANDLING
    
    except socket.timeout:
        # Connection took too long - server may be down or blocking
        return {'error': f'Connection timeout: Unable to reach {domain}'}
    
    except socket.gaierror:
        # DNS resolution failed - domain doesn't exist
        return {'error': f'Invalid domain: {domain} could not be resolved'}
    
    except ssl.SSLCertVerificationError as e:
        # Certificate is invalid, self-signed, or untrusted
        return {'error': f'SSL Certificate Error: {str(e)}'}
    
    except ssl.SSLError as e:
        # General SSL error (handshake failed, protocol mismatch, etc.)
        return {'error': f'SSL Error: {str(e)}'}
    
    except ConnectionRefusedError:
        # Server refused the connection - no SSL service on port 443
        return {'error': f'Connection refused: {domain} may not have HTTPS enabled'}
    
    except Exception as e:
        # Catch any other unexpected errors
        return {'error': f'Unexpected error: {str(e)}'}



# FLASK ROUTES


@app.route('/', methods=['GET', 'POST'])
def index():
    
    
    cert_info = None  # Will hold certificate information
    
    if request.method == 'POST':
        # Get domain from the submitted form
        domain = request.form.get('domain', '').strip()
        
        # Fetch SSL certificate information
        cert_info = get_ssl_certificate_info(domain)
    
    # Render the template with certificate info (if any)
    return render_template('index.html', cert_info=cert_info)



# APPLICATION ENTRY POINT

if __name__ == '__main__':
    # Run Flask development server
    # debug=True enables:
    # - Auto-reload on code changes
    # - Detailed error pages
    # - Interactive debugger
    # Note: Disable debug mode in production!
    app.run(debug=True, host='127.0.0.1', port=5000)
