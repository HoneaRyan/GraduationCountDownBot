''' This script was created to account for one function needing to run
hourly while another had to run daily. This is the daily script that
calculates the time until the closest graduation and then a random 
graduation. It then tweets that value. '''

import GradBot

if __name__ == '__main__':
	graduations = GradBot.getGraduationDates()
	GradBot.createDailyTweet(graduations)