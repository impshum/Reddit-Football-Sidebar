import praw
import configparser
from requests import get


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
reddit_target_subreddit = config['REDDIT']['reddit_target_subreddit']
reddit_widget_name = config['REDDIT']['reddit_widget_name']
football_api_key = config['FOOTBALL']['football_api_key']
football_league_ids = config['FOOTBALL']['football_league_ids'].split(',')


def main():
    reddit = praw.Reddit(
        username=reddit_user,
        password=reddit_pass,
        client_id=reddit_client_id,
        client_secret=reddit_client_secret,
        user_agent='Reddit Sidebar Football (by u/impshum)'
    )

    sub = reddit.subreddit(reddit_target_subreddit)

    old_sidebar_contents = ''
    new_sidebar_contents = ''

    for football_league_id in football_league_ids:

        url = f'https://apiv2.apifootball.com/?action=get_standings&league_id={football_league_id}&APIkey={football_api_key}'
        data = get(url).json()

        old_sidebar = f'&nbsp;|&nbsp;|P|W|D|L\r:-:|:-:|:-:|:-:|:-:|:-:'
        new_sidebar = f'&nbsp;|&nbsp;|MP|W|D|L|GF|GA|PTS\r:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:'

        for team in data:
            country = team['country_name']
            league = team['league_name']
            position = team['overall_league_position']
            name = team['team_name']
            played = team['overall_league_payed']
            won = team['overall_league_W']
            drawn = team['overall_league_D']
            lost = team['overall_league_L']
            gf = team['overall_league_GF']
            ga = team['overall_league_GA']
            pts = team['overall_league_PTS']

            old_sidebar += f'\r{position}|{name}|{played}|{won}|{drawn}|{lost}'
            new_sidebar += f'\r{position}|{name}|{played}|{won}|{drawn}|{lost}|{gf}|{ga}|{pts}'

        old_sidebar_contents += f'## {league} - {country}\n\n{old_sidebar}\n\n'
        new_sidebar_contents += f'## {league} - {country}\n\n{new_sidebar}\n\n'

    sub.wiki['config/sidebar'].edit(old_sidebar_contents)

    for widget in reddit.subreddit(reddit_target_subreddit).widgets.sidebar:
        if widget.shortName.lower() == reddit_widget_name:
            widget.mod.update(text=new_sidebar_contents)


if __name__ == '__main__':
    main()
