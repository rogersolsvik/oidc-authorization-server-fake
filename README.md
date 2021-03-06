# OIDC Authorization Server fake for automatic API testing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a small application that issues valid, but harmless customizable JWT tokens for enabling better testing of API's.
The application also acts as a issuer and authority and supports OIDC discovery mechanisms for token validation.

All cryptographic keys and tokens are only valid as long as the "fake-auth server" is running and will not give access to anything outside of the test setup.

## Why?

I have seen many times that testing API's involves messy configuration in the authorization platform with either long-lived all-access tokens, multiple test-clients or worse, disabling or bypassing security alltogether :scream:. 
I addition to the security risk this approach might impose, you might only be testing your functional requirements and not your authorization logic. You should also test how your API responds to getting "unexpected" tokens.
Examples include:
* Expired tokens
* Tokens with a valid signature, but missing certain claims
* Same as above, but with unexpected values in claim
* Incorrect auduence
* Missing/incorrect scopes
* "Overbloated" tokens

Each project you have might also have differenct requirements in this aspect, and being able to configure and test this from within your solution makes sense. That way each developer does not need to have access to a central authorization platform or rely on an administrator to create and change setup as tests change.

## Roadmap

- [ ] Support secure (TLS) metadata endpoint (discovery) -  Required by OIDC spec and enforced by some libraries
- [ ] Add "vendor specific" token endpoints - read more [here](#vendor-specific-token-endpoints)
- [ ] Configurable algorithm and key-length (uses `RS256` and 2048 bits)
- [ ] Configurable default token claims
- [ ] Cli version? - Might be useful

## How does it work?

The application itself is quite simple and runs as a little web-server hosted in a Docker container. It features endpoints with minimal configuration for:
* ./well-known/openid-configuration -> to support OIDC discovery
* ./well-known/jwks -> contains the public key that applications use for signature validation
* /token -> allows creation of a token pr your definition without requireing authentication

Each time the application starts it generates a new private/public key-pair and holds it in memory. The `/jwks` exposes the public key and all tokens issued are signed with the corresponding private-key. Keys are discarded when the application shuts-down. 
Your application then configures it's `issuer`/`authority` setting and in some cases `audience`, `metadata-endpoint` and `token-endpoint` to use your locally running fake-auth server.
Your tests can create it's tokens using the `/token`-endpoint that will validate correctly using the setup described.

In addition to local developer testing, the motivation was to enable automatic testing in a CI environment. 
Many popular CI server support running so-called "service containers" that are Docker containers running detached in a network shared by your "job". 
Using this technique, your fake auth server can be "provisioned" and isolated for your tests only.

## How to get started

The application is available as a Docker image

```bash
docker run -e OIDC_ISSUER=http://localhost:8080 -p 8080:8080 ghcr.io/rogersolsvik/oidc-authorization-server-fake
```

## Vendor specific token endpoints