#!/usr/bin/env python3
# Server implementation for Google OAuth with MkDocs

import os
import json
import logging
from pathlib import Path
from functools import wraps

from flask import Flask, redirect, request, session, url_for, jsonify, send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# Auth configuration
AUTH_ENABLED = True
ALLOWED_DOMAINS = ['gmail.com']  # Example domain restriction
ALLOWED_EMAILS = []  # Specific emails to allow

# Load configuration from mkdocs.yml if available
try:
    import yaml
    with open('mkdocs.yml', 'r') as f:
        mkdocs_config = yaml.safe_load(f)
        auth_config = mkdocs_config.get('extra', {}).get('auth', {})
        
        if auth_config:
            AUTH_ENABLED = auth_config.get('enabled', True)
            ALLOWED_DOMAINS = auth_config.get('allowed_domains', ALLOWED_DOMAINS)
            ALLOWED_EMAILS = auth_config.get('allowed_emails', ALLOWED_EMAILS)
except Exception as e:
    print(f"Could not load mkdocs.yml: {e}")

# Set up Google OAuth blueprint
google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    scope=["profile", "email"],
    redirect_url="/auth/google/callback"
)
app.register_blueprint(google_bp, url_prefix="/auth")

# Authentication routes
@app.route('/auth/google')
def login():
    return redirect(url_for('google.login'))

@app.route('/auth/google/callback')
def google_callback():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v2/userinfo')
    if resp.ok:
        user_info = resp.json()
        email = user_info.get('email')
        
        # Check domain restrictions
        if email:
            domain = email.split('@')[-1]
            if (not ALLOWED_DOMAINS or domain in ALLOWED_DOMAINS) or \
               (not ALLOWED_EMAILS or email in ALLOWED_EMAILS):
                # Generate token (in a real implementation, use JWT or similar)
                token = generate_token(user_info)
                
                # Return HTML that sets the token in localStorage and redirects
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Authentication Successful</title>
                    <script>
                        localStorage.setItem('mkdocs_google_auth_token', '{token}');
                        const redirect = localStorage.getItem('mkdocs_auth_redirect') || '/';
                        window.location.href = redirect;
                    </script>
                </head>
                <body>
                    <h1>Authentication Successful</h1>
                    <p>Redirecting...</p>
                </body>
                </html>
                """
    
    # Auth failed
    return redirect('/login?error=unauthorized')

@app.route('/auth/verify', methods=['POST'])
def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
    
    token = auth_header.split(' ')[1]
    # Verify token (implement your verification logic here)
    # For a simple example, you could have a list of valid tokens
    
    return jsonify({'valid': True})

@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/login')

# Serve the built mkdocs site
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_site(path):
    # For simplicity in this example, we'll assume the site is built in 'site' directory
    site_dir = Path('site')
    
    # If the path doesn't exist, try adding .html or /index.html
    requested_path = site_dir / path
    if not requested_path.exists():
        if (site_dir / f"{path}.html").exists():
            path = f"{path}.html"
        elif (site_dir / path / "index.html").exists():
            path = f"{path}/index.html"
    
    return send_from_directory('site', path)

# Helper functions
def generate_token(user_info):
    """Generate a simple token for demonstration purposes.
    In production, use a proper JWT or similar authentication approach."""
    import hashlib
    import time
    
    # This is NOT secure for production, just for demo purposes
    token_data = f"{user_info['email']}:{time.time()}:{app.secret_key}"
    return hashlib.sha256(token_data.encode()).hexdigest()

if __name__ == '__main__':
    # Use environment variable PORT if available (for PaaS deployments)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)