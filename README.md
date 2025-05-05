This is a Python-based endpoint availability monitor that reads a YAML configuration file passed as a command-line argument. The YAML format strictly follows the sample provided, including fields like url, method, headers, and body.

The script checks all endpoints every 15 seconds and determines their availability based on two strict conditions:

The HTTP status code must be between 200 and 299.

The response time must be 500 milliseconds or less.

For each check, the script extracts the domain using urlparse().hostname, which ensures that port numbers are ignored. Availability is tracked cumulatively — meaning it calculates overall success over time, not just per cycle.

After every check cycle, it logs an availability report by domain, showing the percentage of successful checks so far. It doesn’t skip or delay cycles based on endpoint response time — the 15-second interval is strictly maintained using time.sleep(15).

This implementation satisfies all the technical requirements, including:

Handling YAML input

Validating status code and latency

Grouping availability by domain

Providing recurring availability logs on a fixed interval

**In the original code, several gaps were addressed:**

No latency check

Port was included in domain

No default HTTP method

No request timeout

Incorrect request body handling

No debug visibility

No user confirmation or YAML validation

I corrected all of these to ensure accurate and resilient endpoint monitoring.

