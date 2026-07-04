import datetime
import json
import logging
import os
from logging.handlers import RotatingFileHandler

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

MAX_BYTES = 10485760  # 10MB
BACKUP_COUNT = 5

def setup_logger(name, filename):
    filepath = os.path.join(LOGS_DIR, filename)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Avoid duplicate handlers
    if not logger.handlers:
        handler = RotatingFileHandler(filepath, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

audit_logger = setup_logger("audit_logger", "audit.log")
security_logger = setup_logger("security_logger", "security.log")
agent_logger = setup_logger("agent_logger", "agent.log")

def log_audit(username: str, action: str, target: str, message: str, banned_until=None):
    payload = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "username": username,
        "action": action,
        "target": target,
        "message": message
    }
    if banned_until:
        payload["banned_until"] = banned_until
    audit_logger.info(json.dumps(payload))

def log_security(username: str, event: str, status: str, details: str = ""):
    payload = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "username": username,
        "event": event,
        "status": status,
        "details": details
    }
    security_logger.info(json.dumps(payload))

def log_agent(node: str, action: str, details: str = ""):
    payload = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "node": node,
        "action": action,
        "details": details
    }
    agent_logger.info(json.dumps(payload))
