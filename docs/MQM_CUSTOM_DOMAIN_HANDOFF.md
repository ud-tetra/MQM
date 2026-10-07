# MQM custom hostname handoff

Prepared: 18 September 2026

Hostname: mqm.udphysics.com
Status when prepared: pending. The existing site remains live until DNS validation and TLS activation finish.

Add these records in the udphysics.com DNS zone, using the provider's relative-name or full-hostname convention:

| Type | Relative name | Value |
|---|---|---|
| CNAME | mqm | custom-domains.chatgpt.site. |
| TXT | _openai-site-verification.mqm | openai-site-verification=8hYC2HHdlJGW5QuUAXI2Vl4KgCowJRaYdSwC6s7g2C4 |
| TXT | _cf-custom-hostname.mqm | 6c5a4421-fd41-41e9-8a2f-71656ca2ffd7 |

Do not replace an existing conflicting mqm record without checking its purpose. DNS provider access is not available in this session; these records have not been written. After they are added, refresh the Sites custom-domain status and wait for active DNS/TLS before announcing the custom URL.
