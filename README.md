# MkDocs Google Authentication

This project integrates Google OAuth authentication with MkDocs, allowing you to secure your documentation site with Google login.

## Features

- Secure documentation with Google OAuth
- Restrict access to specific domains
- Restrict access to specific email addresses
- Simple integration with MkDocs

## Quick Start

1. Clone this repository
2. Install the requirements: `pip install -r requirements.txt`
3. Set up your Google OAuth credentials in the Google Cloud Console
4. Set environment variables for your credentials:
   ```
   export GOOGLE_CLIENT_ID="your_client_id"
   export GOOGLE_CLIENT_SECRET="your_client_secret"
   export SECRET_KEY="your_secret_key"
   ```
5. Build the MkDocs site: `mkdocs build`
6. Run the server: `python server.py`

## Configuration

Edit the `mkdocs.yml` file to configure authentication:

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

See the `.github/workflows/deploy.yml` file for an example GitHub Actions workflow for deployment.

## License

MIT