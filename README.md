I built a Python-based endpoint availability monitor that reads a YAML configuration file passed as a command-line argument. The YAML format exactly matches the sample provided, including fields like url, method, headers, and body.

The script checks all endpoints every 15 seconds and determines their availability based on two strict conditions:

The HTTP status code must be between 200 and 299.

The response time must be 500 milliseconds or less.

For each check, I extract the domain using urlparse().hostname so that port numbers are ignored. The availability is tracked cumulatively — that means the script calculates success over time, not just per cycle.

After every check cycle, the script logs an availability report by domain, showing the percentage of successful checks so far. It doesn’t stop or skip cycles based on how long endpoints take — the 15-second interval is strictly maintained using time.sleep(15).

This approach satisfies all the technical requirements provided, including handling the YAML input, validating the status code and latency, grouping by domain, and providing cumulative, recurring availability logs in a consistent interval.

