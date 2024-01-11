import random
from datetime import datetime, timedelta


def generate_random_value(start, end):
    return random.randint(start, end)


def generate_random_interactions_array():
    array_length = random.randint(4, 10)
    generated_array = []

    for i in range(array_length):
        generated_object = {
            "url": f"https://example.com/{i + 1}",
            "date": generate_random_date(),
            "id": str(i + 1),
        }

        generated_array.append(generated_object)

    return generated_array


def get_default_value(start=100, end=1000):
    # return 0
    # Test only
    return generate_random_value(start, end)


def get_default_interactions():
    # return []
    # Test only
    return generate_random_interactions_array()


def generate_random_date():
    base_date = datetime(2023, 12, 1, 10, 30, 0)
    random_offset = timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    random_date = base_date + random_offset

    return random_date.isoformat()


DEFAULT_METRIC_TOTAL_FOLLOWERS = {
    "title": "Total Followers",
    "slug": "total_followers",
    "values": {"count": get_default_value()},
}
DEFAULT_METRIC_TOTAL_MENTIONS = {
    "title": "Total Mentions",
    "slug": "total_mentions",
    "values": {"count": get_default_value(10, 30)},
}
DEFAULT_METRIC_TOTAL_MENTION_VIEWS = {
    "title": "Total Mention views",
    "slug": "total_mention_views",
    "values": {"count": get_default_value()},
}
DEFAULT_METRIC_TOTAL_USER_INTERACTIONS = {
    "title": "Total Users Interacted",
    "slug": "total_users_interacted",
    "values": {"count": get_default_value()},
}

DEFAULT_LIST_TWEET_INTERACTED_WITH = {
    "title": "Tweets Interacted",
    "slug": "tweets_interacted",
    "values": get_default_interactions(),
}

DEFAULT_AGGREGATE_SUMMARY = {
    "title": "Aggregate Summary",
    "slug": "aggregate_summary",
    "values": {
        "Total Interaction": get_default_value(),
        "Reach and Impression": get_default_value(),
        "Engagement Rate": get_default_value(),
        "Top Performance": get_default_value(),
    },
}

DEFAULT_AGGREGATE_USER_DEMOGRAPHICS = {
    "title": "User Demographics",
    "slug": "user_demographics",
    "values": {
        "Women": get_default_value(),
        "Men": get_default_value(),
    },
}

DEFAULT_CHART_BY_MONTH = {
    "title": "Campaign Report",
    "slug": "campaign_report",
    "values": {
        "Jan": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Feb": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Mar": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Apr": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "May": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Jun": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "July": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Aug": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Sep": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Oct": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Nov": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
        "Dec": {
            "mentions": get_default_value(0, 15000),
            "interactions": get_default_value(0, 15000),
        },
    },
}
