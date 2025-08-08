# harpin AI Code Examples
Examples of integration into the harpin AI product

# Authentication
Most APIs in harpin AI require an access token for authentication.  An access token is obtained via the `/token` API and is valid for 1 hour.  To obtain an access token, you call the `/token` API with a client ID and refresh token.

## Obtaining the client ID and refresh token
Follow these steps in the harpin AI web application to obtain the client ID and refresh token needed to get an access token.
1. Access the harpin AI web application at https://app.harpin.ai
1. Log in to the web application.  If you do not have credentials, reach out to your harpin AI account manager.
1. Once you are logged in, expand the "Settings" menu in the bottom left corner, and then click on the "Account settings" menu item.
1. On the "Account settings" screen, click on the "API credentials" tab.
1. Copy or note the “Client ID” value on this tab.
1. Use the "Generate refresh token" button to obtain a refresh token.  Copy the refresh token somewhere secure as once you leave the screen it cannot be obtained again.  It will need to be regenerated.

## Using the client ID and refresh token
The examples in this repository assume that the client ID and refresh token are stored in environment variables named `CLIENT_ID` and `REFRESH_TOKEN`.  For production usage, the client ID can be stored in configuration if so desired.  However, the refresh token should be stored in a secure location such as a secrets manager.