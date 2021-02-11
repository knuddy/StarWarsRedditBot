import os

CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]

CLIENT_SECRET = os.environ["REDDIT_SECRET"]

PASSWORD = os.environ["REDDIT_PASSWORD"]

USER_AGENT = os.environ["REDDIT_USER_AGENT"]

USERNAME = os.environ["REDDIT_USERNAME"]

DATABASE_URL = os.environ["DATABASE_URL"]

POSTING_ENABLED = os.environ["POSTING_ENABLED"] == "y"

TIME_BETWEEN_POSTS = os.environ["TIME_BETWEEN_POSTS"]

SUBREDDIT_NAME = "all"

SEARCH_TERM = "This is the way"
