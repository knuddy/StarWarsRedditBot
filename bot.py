import praw
import re
import sys
from datetime import datetime, timedelta
from post_template import POST_TEMPLATE
from database import Database


class StarWarsBot:
    def __init__(self, client_id, client_secret, password, user_agent, username, db_url):
        self.reddit_instance = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )
        
        self.username = username

        self.db = Database(db_url)
        self.cached_character_indexs = self.db.character_indexs()

    def run(self, subreddit_name, search_term):
        subreddit = self.reddit_instance.subreddit(subreddit_name)

        for comment in subreddit.stream.comments(skip_existing=True):
            comment_text_lower = comment.body.lower()
            username = comment.author.name

            if username is not self.username and re.search(search_term.lower(), comment_text_lower, re.IGNORECASE):
                self.handle_user_comment(comment, username)



    def handle_user_comment(self, comment, username):
        print(username)
        sys.stdout.flush()
        character_index = username[:2].lower()

        if character_index not in self.cached_character_indexs:
            self.db.create_character_index_and_insert_new_user_score(character_index, username)
            self.cached_character_indexs.append(character_index)
            print("new index")
            sys.stdout.flush()
        else:
            row = self.db.user_data(character_index, username)
            
            if row is not None:
                self.db.update_user_score(character_index, username, row[1], row[2])
                print("update")
                sys.stdout.flush()
            else:
                self.db.add_new_user_to_character_index(character_index, username)
                print("new user")
                sys.stdout.flush()

        if self.db.can_make_new_post():
            self.make_new_post(character_index, username, comment)
            self.db.update_time_since_last_post()

    def make_new_post(self, character_index, username, comment):
        _, usernames, scores = self.db.user_data(character_index, username)
        user_score, _ = self.db.user_score_and_index(username, usernames, scores)

        top_three, user_rank = self.db.top_three_and_user_rank(user_score)

        post_reply = POST_TEMPLATE.format(
            top_three[0][1], top_three[0][0],
            top_three[1][1], top_three[1][0],
            top_three[2][1], top_three[2][0],
            user_rank, username, user_score
        )

        comment.reply(post_reply)


        
