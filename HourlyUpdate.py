''' This script was created to account for one function needing to run
hourly while another had to run daily. This is the hourly script and
it checks to see if any twitter user has posted asking about their
graduation in the last hour and responds to them if they have. '''

import GradBot

if __name__ == '__main__':
	graduations = GradBot.getGraduationDates()
	GradBot.respond(graduations)