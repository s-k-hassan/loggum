# Loggum

A simple log generating program for testing purposes. Used to generate varying log formats to stdout.

## Why?

I needed a way of generating log files for personal testing and learning with various observability services like Datadog and Splunk. While there are definitely other tools out there that are just as good or likely even better, I wanted to be able to have the chance to play with building the code myself and also arbitrarily add or remove different logging formats as needed.

## How to use

Loggum has several key `.env` settings to use to adjust how the generator runs.

- `LOG_COUNT` is the total amount of logs to generate. If you need indefnite log generation, set this to 0. If unset, defaults to 10.
- `SERVER_NAME` is for the hostname will show as when generating the logs. Particularly when using multiple instances, setting different server names will allow you to simulate different hosts in the environment. If unset, defaults to localhost.
- `GENERATOR_FORMAT` sets the format for the logs. Currently created are `CLF`, `JSON`, and `RFC5424`. If unset, defaults to CLF.
- `MINIMUM_WAIT` and `MAXIMUM_WAIT` are used to generate the lower and upper bounds between log generation. Default is zero (immediately create all logs).

These are explained in the `.env.template` file in the repo, which can be used as a default starting point for deployment locally.

## As a Docker container

Loggum can be deployed as a Docker container using the included Docker and Compose files. The associated Compose file can be used to also set varying timezones for the logs generated. To change the `env` variables, uncomment the relevant lines and update them as needed.

## Log Formats

### CLF

The CLF format returns logs in the format `<severity level> <timestamp> <server name> <log message>`

The time format is `mm-dd-yyyy HH:MM:SS timezone`

### RFC5424

The RFC5424 format returns logs in the format `<severity level> <prival> <timestamp> <server name> <tag> <message>`

The time format is `dd-month-yyyy HH:MM:SS timezone` where _month_ is a 3-letter string

### JSON (and STOCKTX)

The `STOCKTX` generator uses JSON to format its logs.

The JSON format returns a minimum of `<severity level> <timestamp>` plus any additional values depending on the generator used. All time formats for JSON are `<dd-month-yyyy HH:MM:SS timezone>` where _month_ is a 3-letter string.
