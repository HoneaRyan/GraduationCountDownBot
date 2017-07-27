''' This TwitterBot AustinPeayGradBot was created by Ryan Honea.

It utilizes the Twitter API to update students with a graduation 
countdown based on the current date and dates in the 
Graduation_Days.txt file

Credit to the creator of the tweepy package for making this process 
incredibly simple. 

I use Python Anywhere's base scheduling feature to run this script 
every day at 8:00 AM Central Time.'''


import tweepy
import time
import csv
from datetime import datetime
from credentials import *
from random import randint
from sys import exit

# These keys come from credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

season_dict = {"spring" : 1, "summer" : 2, "winter" : 3}

# This function deletes a graduation on the day it occurs
def deleteRecentGraduation():
	lines = open("Graduation_Days.txt", 'r').readlines()
	file = open("Graduation_Days.txt", 'w')
	for i in range(1,len(lines)):
		file.write(lines[i])
	file.close()

# This returns at most 1000 tweets that contain @APGradCountDown
def pullLast24Hours():
	query = screen_name
	max_tweets = 1000
	tweets = [tweet for tweet in 
				tweepy.Cursor(api.search, q=query).items(max_tweets)
				if (datetime.now() - tweet.created_at).days < 1]
	return tweets


# This opens the file with the graduation dates and returns them
def getGraduationDates():
	with open("Graduation_Days.txt") as f:
		content = f.readlines()

	graduations = [x.strip().split(',') for x in content]
	return graduations


# This just calculates the days until the selected graduation. Attempt at DRY
def days_until(current_day, current_year, grad_day, grad_year):
	return str((grad_year - current_year)*365 + (grad_day-current_day))



# This creates the daily tweet noting days until closest and random graduation
def createDailyTweet(day, year, graduations):
	tweet_lines = []

	days_until_closest = days_until(
						day, year,
						int(graduations[0][0]),
						int(graduations[0][1]))

	if (days_until_closest == '0'):
		tweet_lines.append("Congratulations to the " + graduations[0][2] 
							+ " class of " + graduations[0][1] + "!")
		deleteRecentGraduation()
	else:
		# Creates part of tweet for closest graduation
		tweet_lines.append(days_until_closest + " days until the " 
							+ graduations[0][1] + " " 
							+ graduations[0][2] + "!")


		# Creates part of tweet for random future graduation
		rand = randint(1,len(graduations)-1)
		days_until_rand = days_until(
						day, year,
						int(graduations[rand][0]),
						int(graduations[rand][1]))

		tweet_lines.append(days_until_rand + " days until the " 
							+ graduations[rand][1] + " " 
							+ graduations[rand][2] + "!")

	
	tweet_lines.append('#AustinPeay #CollegeGraduation')

	status = '\n'.join(tweet_lines)
	post_tweet(status)



# This first collects 1000 tweets from the last 24 hours and checks to see if
# any match the criterion for a response. If they tweet with the following
# format: [@APGradCountDown season yyyy] then a response will be made with 
# how many days they have until they graduate.
def respond(day, year, graduations):
	latest_tweets = pullLast24Hours()
	min_year = graduations[0][1]
	max_year = graduations[-1][1]
	min_season = season_dict[graduations[0][2].split()[0].lower()]
	max_season = season_dict[graduations[-1][2].split()[0].lower()]
	for tweet in latest_tweets:
		days_until_grad = ''
		status = tweet.text.split()
		response = '@' + str(tweet.user.screen_name) + ' '
		tweetId = tweet.id
		if len(status) != 3: break
		season = status[1].lower()
		season_key = season_dict[season]
		status_year = status[2]
		if season == 'spring' or season == 'winter' or season == 'summer':
			if (status_year > max_year or
					(status_year == year and season_key > max_season)):
				response = response + 'You\'ve got a long way to go!'
			elif (status_year < min_year or
					(status_year == year and season_key < min_season)):
				response = response + 'You already graduated!'
			else:
				for graduation in graduations:
					if (graduation[1] == status_year
							and graduation[2].split()[0].lower() == season):
						days_until_grad = days_until(
										day, year,
										int(graduation[0]),int(graduation[1]))
				if days_until_grad == '': 
					response += 'Your graduation is not on record. Sorry!'
				else:
					response += "You graduate in " + days_until_grad + " days!"
			reply(response, tweetId)


# This uses the API to post the tweet
def post_tweet(status):
	# print(status)
	api.update_status(status)

# This happens when a reply is made so it lists as a reply
def reply(status, tweetId):
	# print(status)
	api.update_status(status, tweetId)


if __name__ == '__main__':
	day_of_year = datetime.now().timetuple().tm_yday
	current_year = int(datetime.now().year)

	graduations = getGraduationDates()
	createDailyTweet(day_of_year, current_year, graduations)
	respond(day_of_year, current_year, graduations)