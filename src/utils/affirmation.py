def calculate_time_difference_seconds(start_at, end_date):
    # Calculate the time difference in seconds
    time_difference_seconds = (end_date - start_at).total_seconds()

    return time_difference_seconds
