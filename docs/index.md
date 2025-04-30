# Welcome to MkDocs with Google Authentication

This is a sample MkDocs site that integrates Google Authentication.

## Features

- Secure documentation with Google OAuth
- Restrict access to specific domains
- Restrict access to specific email addresses
- Simple integration with MkDocs

## Getting Started

To get started, you need to:

1. Set up your Google OAuth credentials
2. Configure the `mkdocs.yml` file
3. Deploy your site

See the [Setup](setup.md) page for detailed instructions.

## How It Works

This integration uses Flask and Flask-Dance to handle Google OAuth authentication. The authentication flow works as follows:

1. When a user visits any page, the client-side JavaScript checks if they have a valid token
2. If no valid token is found, they are redirected to the login page
3. When they click "Sign in with Google", they are redirected to Google's OAuth consent screen
4. After successful authentication, Google redirects back to our callback URL
5. We verify the user's email domain and create a token
6. The token is stored in the browser's localStorage
7. The user is redirected to the page they originally requested

## Adding a Logout Button

You can add a logout button to your MkDocs site by adding the following HTML to your Markdown files:

```html
<button onclick="logout()" class="md-button">Logout</button>
```

## Configuration Options

In your `mkdocs.yml` file, you can configure the authentication settings:

```yaml
extra:
  auth:
    enabled: true  # Set to false to disable authentication
    allowed_domains:
      - yourdomain.com
      - example.com
    allowed_emails:
      - specific.user@gmail.com
```