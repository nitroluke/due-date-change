from datetime import timedelta
from dateutil.relativedelta import relativedelta

def print_rules():
    print("Rules: ")
    print("    25 day rule:  only allow days 1-25.")
    print("    14 day from now rule: New due date must be greater than 14 days from now.")
    print("    next_due > 15 rule:  If the next due date is greater than 15 days from now their new due date must be \n"
          "        45 days from their last satisfied item.")
    print("    next_due <= 15 rule:  If the next due date is less than 15 days from now keep the payment and the new\n"
          "        due date must be 14 days from their next due date and less than 46 days from the next.")


def print_valid_dates(valid_dates, prototype):
    print("{}: ".format(prototype))
    for rule_applied in valid_dates:
        print("    {:<21} ".format(rule_applied) + ": {}".format(valid_dates[rule_applied]))


def date_generator(start_date):
    from_date = start_date
    while True:
        yield from_date
        from_date = from_date + timedelta(days=1)


def next_possible_due_date(due_date):
    return due_date + relativedelta(months=1)
