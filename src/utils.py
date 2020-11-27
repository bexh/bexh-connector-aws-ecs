from datetime import datetime


def get_current_utc_iso() -> str:
    dt = datetime.utcnow()
    return dt_to_iso(dt)


def dt_to_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_to_mysql_format(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    return d.strftime("%Y-%m-%d %H:%M:%S")
