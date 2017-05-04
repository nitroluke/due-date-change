from datetime import timedelta, date
from dueDateUtils import next_possible_due_date


debug = False


def pick_date(proposed_due_day: int, today: date, last_satisfied: date, next_due: date, max_day_of_month: int) -> date:
    if proposed_due_day > max_day_of_month:
        if debug:
            print("cannot get new due day greater than {}".format(max_day_of_month))
        return None
    if proposed_due_day == last_satisfied.day:
        if debug:
            print("cannot change due date to the same as it was before")
        return None
    min_due_date = get_min_proposed_date(today + timedelta(days=15), proposed_due_day)
    if last_satisfied > today:
        min_due_date = last_satisfied.replace(day=proposed_due_day)
    if debug:
        print("min_due_date: {}".format(min_due_date))
        print("max_due_date: {}".format(next_due + timedelta(days=45)))
    rules = get_rules(today, last_satisfied, next_due, min_due_date)
    if debug:
        print(rules)
    max_tries = 3
    tries = 1
    rules_result = check_rules(rules)[0]
    while not rules_result:
        if tries <= max_tries:
            min_due_date = next_possible_due_date(min_due_date)  # min_due_date + relativedelta(months=1)
            rules_result = get_rules(today, last_satisfied, next_due, min_due_date)
            tries += 1
        else:
            if debug:
                print("number of tries exceeded with no solution")
            return None
    return min_due_date


def get_min_proposed_date(min_due_date, proposed_due_day):
    while min_due_date.day != proposed_due_day:
        min_due_date = min_due_date + timedelta(days=1)
    return min_due_date


def check_rules(rules) -> tuple:
    if rules["less_than_or_equal_15_days_til_next_payment"]:
        if debug:
            print("keep payment")
        if rules["15_days_after_next_payment"] and rules["days_from_next_due"]:
            if debug:
                print("batched change")
            return True, True
        else:
            if debug:
                print("does not fall between 15 days after next payment and 45 days from next due:")
                print("    {} -- {}".format(rules["15_days_after_next_payment"], rules["days_from_next_due"]))
    elif rules["more_than_15_days_til_next_payment"]:
        if debug:
            print("no need to keep payment, immediate change")
        if rules["days_from_last_satisfied"]:
            return True, False
        else:
            if debug:
                print("too many days from last satisfied")
    return False, False


def get_rules(today, last_satisfied, next_due, min_due_date) -> dict:
    rules = {
        "15_days_after_today": is_num_days_after(today, min_due_date, 15, "15_days_after_today"),
        "15_days_after_next_payment": is_num_days_after(next_due, min_due_date, 15, "15_days_after_next_payment"),
        "less_than_or_equal_15_days_til_next_payment": is_within_num_days(today, next_due, 15, "less_than_or_equal_15_days_til_next_payment"),
        "more_than_15_days_til_next_payment": num_days_til(today, next_due,   "more_than_15_days_til_next_payment") > 15,
        "days_from_last_satisfied": is_within_num_days(last_satisfied, min_due_date, 45, "days_from_last_satisfied"),
        "days_from_next_due": is_within_num_days(next_due, min_due_date, 45, "days_from_next_due")
    }
    return rules


def num_days_til(start_date: date, end_date: date, rule_name:str) -> int:
    if debug:
        print("{}:".format(rule_name))
        print("    {} - s{} == {}".format(end_date, start_date, (end_date - start_date).days))
    return (end_date - start_date).days


def is_num_days_after(from_date: date, proposed_date, num_days: int, rule_name: str) -> bool:
    if debug:
        print("{}:".format(rule_name))
        print("    {} >= ({} + {} days) == {}".format(proposed_date, from_date, num_days,
                                             proposed_date >= (from_date + timedelta(num_days))))
    return proposed_date >= (from_date + timedelta(days=num_days))


def is_within_num_days(from_date: date, check_date: date, num_days: int, rule_name: str) -> bool:
    if debug:
        print("{}:".format(rule_name))
        print("    {} <= ({} + {} days) == {}".format(check_date, from_date, timedelta(days=num_days),
                                             check_date <= (from_date + timedelta(days=num_days))))
    return check_date <= (from_date + timedelta(days=num_days))
