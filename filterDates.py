from datetime import timedelta, date
from dateutil.relativedelta import *
from itertools import islice
from dueDateUtils import date_generator

debug = False


def filter_dates(now: date, last_satisfied: date, next_due: date, max_day_in_month: int) -> dict:
    valid_dates = {}
    beginning_of_next_mo = (now + relativedelta(months=1)).replace(day=1)
    days_to_25th = ((now.replace(day=max_day_in_month) + timedelta(days=1)) - now).days
    this_month = list(islice(date_generator(now), days_to_25th))
    next_month = list(islice(date_generator(beginning_of_next_mo), max_day_in_month))
    last_month = list(islice(date_generator(beginning_of_next_mo + relativedelta(months=1)), max_day_in_month))
    valid_dates["25 day Rule"] = this_month + next_month + last_month
    if debug:
        print("next_due is {} days from now".format((next_due - now).days))
        print("45 days from last_satisfied = {}".format(last_satisfied + timedelta(days=45)))
        print("45 days from next_due = {}".format(next_due + timedelta(days=45)))
    valid_dates["14 day from now Rule"] = filter_before_date(now, this_month + next_month + last_month, 15)
    if (next_due - now).days >= 16:
        valid_dates["next_due > 15 Rule"] = filter_after_date(last_satisfied, valid_dates["14 day from now Rule"],
                                                              45)
    elif (next_due - now).days < 16:
        fourteen_from_next_due_rule = filter_before_date(next_due, next_month + last_month, 14)
        valid_dates["next_due < 15 Rule:"] = filter_after_date(next_due, fourteen_from_next_due_rule, 45)
    else:
        print("wat")
    return valid_dates


def filter_after_date(from_date: date, list_of_dates: list, days_after_start:int) -> list:
    if debug:
        print("from_date: {} + {} = {}".format(from_date, days_after_start, from_date + timedelta(days=days_after_start)))
    return [x for x in list_of_dates if (x < (from_date + timedelta(days=days_after_start)))]


def filter_before_date(from_date: date, list_of_dates: list, days_after_start:int) -> list:
    if debug:
        print("from_date: {} + {} = {}".format(from_date, days_after_start, from_date + timedelta(days=days_after_start)))
    return [x for x in list_of_dates if not (x < (from_date + timedelta(days=days_after_start)))]