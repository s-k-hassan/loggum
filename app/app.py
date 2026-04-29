import logging, logging.config
import time, random, os
import yaml, dotenv
import logClasses
import pythonjsonlogger

# Load environment variables and validate them
dotenv.load_dotenv()
count = os.environ.get("LOG_COUNT", 1)
servername = os.environ.get("SERVER_NAME", "localhost")
generatorFormat = os.environ.get("GENERATOR_FORMAT", "CLF")
minimumWait = os.environ.get("MINIMUM_WAIT", 0)
maximumWait = os.environ.get("MAXIMUM_WAIT", 0)

# Validate environment variables
assert minimumWait.replace(".", "").isdigit(), "MINIMUM_WAIT must be a numeric value"
assert maximumWait.replace(".", "").isdigit(), "MAXIMUM_WAIT must be a numeric value"
assert float(minimumWait) >= 0, "MINIMUM_WAIT must be a non-negative value"
assert float(maximumWait) >= 0, "MAXIMUM_WAIT must be a non-negative value"
assert float(maximumWait) >= float(
    minimumWait
), "MAXIMUM_WAIT must be greater than or equal to MINIMUM_WAIT"
assert count.isdigit(), "LOG_COUNT must be an integer value"
assert int(count) >= 0, "LOG_COUNT must be a non-negative integer"
assert generatorFormat in [
    "CLF",
    "RFC5424",
    "JSON",
    "STOCKTX",
], "GENERATOR_FORMAT must be one of 'CLF', 'RFC5424', 'JSON', or 'STOCKTX'"
assert servername.isascii(), "SERVER_NAME must be an ASCII string"

# Load logging configuration
# config_file = 'logging_config.yaml'
with open("app/logging_config.yaml", "r") as configFile:
    config = yaml.safe_load(configFile.read())
    logging.config.dictConfig(config)


# Generate log entries based on the specified format
def logGenerator():
    match generatorFormat:
        case "CLF":
            createdLog = logClasses.CLF().generate_log_entry()
            logging.getLogger("loggerCLF").log(
                msg=createdLog[0], level=createdLog[1], extra={"servername": servername}
            )
        case "RFC5424":
            createdLog = logClasses.RFC5424().generate_log_entry()
            logging.getLogger("loggerRFC5424").log(
                msg=createdLog[0],
                level=createdLog[1],
                extra={
                    "prival": createdLog[2],
                    "tag": createdLog[3],
                    "servername": servername,
                },
            )
        case "JSON":
            createdLog = logClasses.JSON().generate_log_entry()
            logging.getLogger("loggerJSON").log(
                msg=createdLog[0],
                level=createdLog[1],
                extra={
                    "sourceip": createdLog[2],
                    "username": createdLog[3],
                    "servername": servername,
                },
            )
        case "STOCKTX":
            createdLog = logClasses.stockTX().generate_log_entry()
            logging.getLogger("loggerJSON").log(
                msg=createdLog, level=createdLog["level"]
            )
    if float(maximumWait) > 0:
        time.sleep(random.uniform(float(minimumWait), float(maximumWait)))


if __name__ == "__main__":
    logging.getLogger("loggerBaseformatter").info(
        f"Log generation started with format: {generatorFormat} and count: {count}"
    )
    logging.getLogger("loggerBaseformatter").info(
        f"Environment variables - SERVER_NAME: {servername}, GENERATOR_FORMAT: {generatorFormat}"
    )

    # Generate logs based on the specified count. If count is 0, generate logs indefinitely
    count = int(count)
    if count > 0:
        for i in range(count):
            logGenerator()
    else:
        while True:
            logGenerator()
