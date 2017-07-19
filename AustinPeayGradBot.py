''' This TwitterBot AustinPeayGradBot was created by Ryan Honea.

It utilizes the Twitter API to update students with a graduation countdown
based on the current date and dates in the Graduation_Days.txt file

Credit to the creator of the tweepy package for making this process incredibly
simple. 

I use Python Anywhere's base scheduling feature to run this script every
day at 12:00 PM Central Time.'''


from sys import exit
from credentials import *
import tweepy
import time
from datetime import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def deleteRecentGraduation():
	lines = open("Graduation_Days.txt", 'r').readlines()
	file = open("Graduation_Days.txt", 'w')
	for i in range(1,len(lines)):
		file.write(lines[i])
	file.close()


day_of_year = datetime.now().timetuple().tm_yday
current_year = int(datetime.now().year)
graduation_days = open("Graduation_Days.txt", 'r')
grad_day = ['','','']
grad_type = ['','','']
grad_year = ['','','']
tweet_lines = []
for i in range(0,2):
	grad_day[i], grad_year[i], grad_type[i] = graduation_days.readline().rstrip('\n').split(',')
	grad_day[i] = str((int(grad_year[i]) - current_year)*365 + (int(grad_day[i])-day_of_year))
	tweet_lines.append(grad_day[i] + " days until the " + grad_year[i] + " " + grad_type[i] + "!")

graduation_days.close()

if (grad_day[0] == '0'):
	tweet = "Congratulations to the " + grad_type[0] + " class of " + grad_year[0] + "!"
	deleteRecentGraduation()
else:
	tweet = "\n".join(tweet_lines)

tweet += "\n#AustinPeay #CollegeGraduation"

api.update_status(status=tweet)