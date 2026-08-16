# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (`main`) | ✅ |

## Reporting a Vulnerability

If you discover a security vulnerability in TeraBridge API, **please do not open a public GitHub issue**. Public disclosure of security issues before a fix is available puts all users at risk.

Instead, report it privately via one of the following:

- **GitHub Private Vulnerability Reporting:** Use the [Report a vulnerability](../../security/advisories/new) button on the Security tab of this repository.
- **Email:** If you prefer email, open a GitHub issue asking for a private contact and we will respond within 48 hours.

## What to Include

To help resolve the issue quickly, please include:

- A clear description of the vulnerability
- Steps to reproduce or a proof-of-concept
- The potential impact (e.g., credential exposure, SSRF, auth bypass)
- Any suggested fix if you have one

## Scope

Security issues relevant to this project include:

- **API key or HMAC secret exposure** — anything that could leak or bypass authentication
- **SSRF vulnerabilities** — bypassing the domain allowlist in the segment proxy
- **Cookie/session leakage** — Terabox session credentials being exposed in responses, logs, or errors
- **Rate limiter bypass** — techniques to circumvent per-IP request limiting
- **Dependency vulnerabilities** — critical CVEs in `fastapi`, `httpx`, `uvicorn`, or other direct dependencies

## Out of Scope

- Issues requiring physical access to the server
- Social engineering attacks
- Vulnerabilities in Terabox itself (report those to Terabox directly)
- Self-hosted deployments with intentionally weakened configuration (e.g., `REQUIRE_API_KEY=0` in production)

## Response Timeline

| Stage | Target |
|-------|--------|
| Initial acknowledgement | Within 48 hours |
| Triage and severity assessment | Within 5 business days |
| Fix or mitigation | Depends on severity — critical issues are prioritised |
| Public disclosure | After fix is released |

## Responsible Disclosure

We follow responsible disclosure practices. If you report a valid vulnerability, we will credit you in the release notes unless you prefer to remain anonymous.
