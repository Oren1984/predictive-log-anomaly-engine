"""Stage 2 — Parsing: log parser interface and minimal implementations."""
import json
import re
from abc import ABC, abstractmethod

from src.data_layer.models import LogEvent


class LogParser(ABC):
    """Interface: parse a raw log string into a LogEvent."""

    @abstractmethod
    def parse(self, raw: str) -> LogEvent:
        ...


# ---------------------------------------------------------------------------
class RegexLogParser(LogParser):
    """
    Generic regex-based parser.

    Default pattern matches lines like:
        2005-12-01 06:51:06 INFO dfs.DataNode: message here
    Groups: timestamp, level, message  (service left empty by default).
    """

    _DEFAULT = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}[\s\-]\d{2}[:.]\d{2}[:.]\d{2}[.\d]*)?"
        r"\s*(?P<level>INFO|WARN|ERROR|FATAL|DEBUG|TRACE)?\s*"
        r"(?P<message>.+)",
        re.IGNORECASE,
    )

    def __init__(self, pattern: re.Pattern = None, service: str = ""):
        self._pattern = pattern or self._DEFAULT
        self._service = service

    def parse(self, raw: str) -> LogEvent:
        m = self._pattern.search(raw.strip())
        if m:
            gd = m.groupdict()
            return LogEvent(
                timestamp=None,
                service=self._service,
                level=(gd.get("level") or "").upper(),
                message=(gd.get("message") or raw).strip(),
            )
        return LogEvent(timestamp=None, service=self._service,
                        level="", message=raw.strip())


# ---------------------------------------------------------------------------
class JsonLogParser(LogParser):
    """
    Parser for JSON-structured log lines.

    Expects keys: 'timestamp', 'level'/'severity', 'message'/'msg'.
    Any other keys go into meta.
    """

    def __init__(self, service: str = ""):
        self._service = service

    def parse(self, raw: str) -> LogEvent:
        try:
            obj = json.loads(raw.strip())
        except json.JSONDecodeError:
            return LogEvent(timestamp=None, service=self._service,
                            level="", message=raw.strip())

        ts      = obj.pop("timestamp", obj.pop("ts", None))
        level   = obj.pop("level", obj.pop("severity", "")).upper()
        message = obj.pop("message", obj.pop("msg", raw.strip()))
        label   = obj.pop("label", None)

        return LogEvent(
            timestamp=float(ts) if ts is not None else None,
            service=obj.pop("service", self._service),
            level=level,
            message=str(message),
            meta=obj,
            label=int(label) if label is not None else None,
        )
