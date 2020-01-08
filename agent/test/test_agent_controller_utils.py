from agents.prediction_market_adapter import NUM_PREDICTIONS


def only_once_during_first_half_day(func, period_offset=0):
    picked_time = False
    for period in range(NUM_PREDICTIONS // 2):
        if func(period_offset + period):
            # may only pick one time
            if picked_time:
                return False
            picked_time = True

    # must pick a time during first half of the day
    for period in range(NUM_PREDICTIONS // 2, NUM_PREDICTIONS):
        if func(period_offset + period):
            return False

    return picked_time


def only_once_during_second_half_day(func, period_offset=0):
    # must pick time during second half of the day
    for period in range(NUM_PREDICTIONS // 2):
        if func(period_offset + period):
            return False

    picked_time = False
    for period in range(NUM_PREDICTIONS // 2, NUM_PREDICTIONS):
        if func(period_offset + period):
            # may only pick one time
            if picked_time:
                return False
            picked_time = True

    return picked_time


def first_this_then_that(func1, func2, period_offset=0):
    more_first = False
    for period in range(NUM_PREDICTIONS):
        if func1(period_offset + period):
            more_first = True
        if func2(period_offset + period):
            if not more_first:
                return False
            else:
                more_first = False

    return not more_first
