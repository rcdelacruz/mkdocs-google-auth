# Setup Guide

## Prerequisites

- Python 3.7+
- MkDocs
- MkDocs Material theme
- Google Cloud Platform account

## Installation

1. Install required packages:

```bash
pip install mkdocs mkdocs-material mkdocs-macros-plugin mkdocs-simple-hooks flask-dance
```

2. Clone this repository:

```bash
git clone https://github.com/yourusername/mkdocs-google-auth.git
cd mkdocs-google-auth
```

## Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to APIs & Services > Credentials
4. Click "Create Credentials" and select "OAuth client ID"
5. Configure the OAuth consent screen:
   - Add your app name
   - Add your domain
   - Add the scopes for email and profile
6. Create OAuth client ID:
   - Application type: Web application
   - Name: MkDocs Auth
   - Authorized JavaScript origins: Your site URL (e.g., `https://yourdocs.example.com`)
   - Authorized redirect URIs: Your site URL + `/auth/google/callback` (e.g., `https://yourdocs.example.com/auth/google/callback`)
7. Note down your Client ID and Client Secret

## Configuration

1. Create environment variables for your Google OAuth credentials:

```bash
export GOOGLE_CLIENT_ID="your_client_id"
export GOOGLE_CLIENT_SECRET="your_client_secret"
export SECRET_KEY="random_secure_secret_key"
```

2. Update `mkdocs.yml` with your authentication settings:

```yaml
extra:
  auth:
    enabled: true
    allowed_domains:
      - yourdomain.com
    allowed_emails:
      - specific.user@gmail.com
```

## Deployment

You can deploy this site to any platform that supports Python applications. Some common options are:

### 1. Use Docker

The repository includes a Dockerfile for easy containerization:

```bash
# Build the Docker image
docker build -t mkdocs-google-auth .

# Run the container
docker run -p 5000:5000 \
  -e GOOGLE_CLIENT_ID="your_client_id" \
  -e GOOGLE_CLIENT_SECRET="your_client_secret" \
  -e SECRET_KEY="your_secret_key" \
  mkdocs-google-auth
```

### 2. Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-mkdocs-site
heroku config:set GOOGLE_CLIENT_ID="your_client_id"
heroku config:set GOOGLE_CLIENT_SECRET="your_client_secret"
heroku config:set SECRET_KEY="your_secret_key"
git push heroku master
```

### 3. Deploy to GitHub Pages with a Separate Authentication Server

You can also deploy the static MkDocs site to GitHub Pages and run the authentication server separately:

1. Use GitHub Actions to build and deploy the static site (see `.github/workflows/deploy.yml`)
2. Run the authentication server on a separate platform (e.g., Heroku, Digital Ocean)
3. Configure your domain to route authentication requests to the server

## Local Development

For local development, you can run:

```bash
# Build the MkDocs site
mkdocs build

# Run the server
python server.py
```

The server will run on http://localhost:5000 by default.