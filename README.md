### API Rate Limiting Bypass Leading to Unlimited Access to Premium Features in explorer.globe.engineer

# Legal and Ethical Disclaimer:
WARNING: This publication is solely for educational purposes and aims to increase awareness of web application security. The author is not responsible for any improper use of the information presented.

Disclaimers:
This article does not contain direct tools enabling exploitation of the described vulnerabilities
Model names and specific API endpoint have been modified
This publication complies with Responsible Disclosure principles
The purpose is solely education and raising security awareness

# Disclosure Timeline:
 02.11.2024 - Informed the site creators directly via the provided email address
 
 04.11.2024 - After no response, informed about the message on Discord platform. Received confirmation that the team would look into the issue
 
 10.12.2024 - After continued lack of response, informed about planned article publication
 
 06.07.2025 - Article publication date (continued lack of response from the team)
 
Despite following all steps regarding secure and responsible disclosure of security vulnerability information, as of the publication date (06.07.2025) the vulnerability remains active.

CVSS Score: 7.5 (High) - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
Vulnerability Type: Authorization Bypass + Rate Limiting Evasion Root Cause: Lack of server-side validation.

# Vulnerability Description:
While using the website, out of curiosity I examined the network connections. During searching, I noticed a request sent to the domain example.dev.api, which later turned out to be an API (first mistake - visible frontend to backend communication).
After analyzing the request, I identified the following parameters:
find_id

find_query

id_user

id_local

model=X

# Exploitation Process:
Parameter Identification: The first step was checking the possibility of modifying the content of the find_query="example" parameter
Bypass Attempt: I changed the value from model=basic to model=premium (the premium model was supposed to contain only 5 free uses)
Successful Bypass: The system accepted the request without any authorization verification

Verification: I received a response on screen confirming access to premium features

# Proof of Concept Implementation
The next step was writing a simple Python script enabling unlimited generation of premium content for free locally. Key implementation elements:

Setting response.headers['Access-Control-Allow-Origin'] = '*'
 Random generation of new find_id with each query
 API connection using appropriately formatted URL.

# Sample URLs (anonymized):
Premium Mode:
https://example.dev.api/submitSearch?queryData=[...anonymized...]&id_user=XXXX&id_local=XXXX&model=premium&find_id={find_id}
Research Premium Mode:
url = f"https://example.dev.api/submitSearch?query={encoded_query}\",[...anonymized...]&id_user=XXXX&id_local=XXXX&model=research_premium&find_id={find_id}

# Technical Implementation:
Since responses were transmitted in Server-Sent Events (SSE) format, I created a simple HTML file with JavaScript code to interpret the received values.

Note: Specific implementation details have been omitted for security reasons, but here is a Proof of Concept (POC): https://youtu.be/7v2pxOsN56U 

# Summary:
The described vulnerability enables:

Bypassing rate limiting restrictions

Unlimited access to premium and research premium features

Resource utilization without proper authorization

Commercial exploitation and unfair competition: The vulnerability enables third parties to create competing services or resell premium features without authorization, potentially undermining the original service's business model

# Key Recommendations for Patching the Vulnerability:

Implement server-side verification: Check user permissions before processing requests
 Hide backend logic: Avoid exposing internal API endpoints
 
 Implement proper rate limiting: Protection at server level, not just client-side
 
 Monitoring and logging: Track unusual usage patterns

## This article was prepared in accordance with Responsible Disclosure principles and is solely for educational purposes.
