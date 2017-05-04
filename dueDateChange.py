from datetime import date, timedelta
from filterDates import filter_dates
from greedyDatePicker import pick_date
from dueDateUtils import print_rules, print_valid_dates

debug = False


def main():
    """
    rules:
        - new_due_day > 14 days from now()
        - only days 1-25 are valid.
        - if next_due_date - now() >= 16
            new_due_date must be < 46 days of last satisfied scheduled item
        - else if next_due_date - now < 16
            - keep payment and new_due_date must be > 14 days from next_due_date and < 46 days from next_due_date
    """
    if debug:
        print_rules()
    today = date(2017, 4, 1)
    last_satisfied = date(2017, 4, 1)
    next_due = date(2017, 5, 1)
    print_valid_dates(filter_dates(today, last_satisfied, next_due, 25), "filter-dates")
    print("old due day: {}".format(last_satisfied))

    for today_mock in [today + timedelta(days=x) for x in range(0, today.max.day)]:
        print("today: {}".format(today_mock))
        for day in range(1, 26):
            new_due_date = pick_date(day, today_mock, last_satisfied, next_due, 25)
            print("    proposed_day: {} :::: new due date: {}".format(day, new_due_date,))


if __name__ == '__main__':
    main()
