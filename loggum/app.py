import logging, logging.config
from pathlib import Path
import time, random, os
import yaml, dotenv
import logClasses

# Import OTel logging libraries
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

baseDir = Path(__file__).resolve().parent
config_path = baseDir / "logging_config.yaml"

# Load environment variables and validate them
dotenv.load_dotenv()
count = os.getenv("LOG_COUNT", 10)
servername = os.getenv("SERVER_NAME", "localhost")
generatorFormat = os.getenv("GENERATOR_FORMAT", "CLF")
minimumWait = os.getenv("MINIMUM_WAIT", 0)
maximumWait = os.getenv("MAXIMUM_WAIT", 0)
otelEndpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "none")

# Validate environment variables
print(
    f"Environment variables - SERVER_NAME: {servername}, GENERATOR_FORMAT: {generatorFormat}, MINIMUM_WAIT: {minimumWait}, MAXIMUM_WAIT: {maximumWait}, LOG_COUNT: {count}"
)
assert float(minimumWait) >= 0, "MINIMUM_WAIT must be a non-negative value"
assert float(maximumWait) >= 0, "MAXIMUM_WAIT must be a non-negative value"
assert float(maximumWait) >= float(
    minimumWait
), "MAXIMUM_WAIT must be greater than or equal to MINIMUM_WAIT"
assert int(count) >= 0, "LOG_COUNT must be a non-negative integer"
assert generatorFormat in [
    "CLF",
    "RFC5424",
    "JSON",
    "STOCKTX",
], "GENERATOR_FORMAT must be one of 'CLF', 'RFC5424', 'JSON', or 'STOCKTX'"
assert servername.isascii(), "SERVER_NAME must be an ASCII string"

# Setup OTel logging provider
if otelEndpoint != "none":
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)
    exporter = OTLPLogExporter(endpoint=otelEndpoint, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Load logging configuration
# config_file = 'logging_config.yaml'
with open(config_path, "r") as configFile:
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
                msg=createdLog,
                level=createdLog["level"],
                extra={"servername": servername},
            )
        case "STOCKTX":
            createdLog = logClasses.stockTX().generate_log_entry()
            logging.getLogger("loggerJSON").log(
                msg=createdLog, level=createdLog["level"]
            )
    if float(maximumWait) > 0:
        time.sleep(random.uniform(float(minimumWait), float(maximumWait)))

def startApp(count, servername, generatorFormat):
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


if __name__ == "__main__":
    startApp(count, servername, generatorFormat)