import dbus
import dbus.service
from calendar import timegm
from dbus.mainloop.glib import DBusGMainLoop as DBusMainLoop
from hamster.lib import datetime as dt
from hamster.lib.fact import Fact


"""D-Bus communication utilities."""

# dates

def from_dbus_date(dbus_date):
    """Convert D-Bus timestamp (seconds since epoch) to date."""
    return dt.date.fromtimestamp(dbus_date) if dbus_date else None


def to_dbus_date(date):
    """Convert date to D-Bus timestamp (seconds since epoch)."""
    return timegm(date.timetuple()) if date else 0


# facts

"""
dbus_fact signature (types matching the to_dbus_fact output)
    i  id
    i  start_time
    i  end_time
    s  description
    s  activity name
    i  activity id
    s  category name
    as List of fact tags
    i  date
    i  delta
"""
fact_signature = '(iiissisasii)'


def from_dbus_fact(dbus_fact):
    """unpack the struct into a proper dict"""
    return Fact(activity=dbus_fact[4],
                start_time=dt.datetime.utcfromtimestamp(dbus_fact[1]),
                end_time=dt.datetime.utcfromtimestamp(dbus_fact[2]) if dbus_fact[2] else None,
                description=dbus_fact[3],
                activity_id=dbus_fact[5],
                category=dbus_fact[6],
                tags=dbus_fact[7],
                id=dbus_fact[0]
                )


def to_dbus_fact(fact):
    """Perform Fact conversion to D-Bus.

    Return the corresponding dbus structure, with supported data types.
    """
    return (fact.id or 0,
            timegm(fact.start_time.timetuple()),
            timegm(fact.end_time.timetuple()) if fact.end_time else 0,
            fact.description or '',
            fact.activity or '',
            fact.activity_id or 0,
            fact.category or '',
            dbus.Array(fact.tags, signature = 's'),
            to_dbus_date(fact.date),
            fact.delta.days * 24 * 60 * 60 + fact.delta.seconds)
