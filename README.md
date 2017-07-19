# GraduationCountDownBot
## Introduction
This bots script runs every day at noon using a PythonAnywhere scheduler. It takes the current day and year and calculates the days until the next graduation. It then tweets that information to students. The graduation days come from the Graduation_Days.txt file. 

On days that a graduation is occurring, it congratulates the class of the year and doesn't inform of any impending graduations. That day is for the graduates after all!

## Extending this to your own University
The first step in using this TwitterBot is setting up an app on your selected twitter accounts with [Twitter Apps](https://apps.twitter.com/). After you have created and named your app, you will need to create a credentials file. You can also include the credentials in the script, but this is in case you ever decide to share any updates, you can add the credentials file to your .gitignore. 
Copy-Paste below into credentials.py:
``` python
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```
The consumer_key and consumer_secret should be immediately accessible on your app on the Twitter Apps site. At the bottom of the page, you will be able to generate the access_token and access_token_secret. Copy all four of those into the quotations.

After you've completed that, you will need to edit the Graduation_Days.txt file. The schema of the file is
DayOfYear,Year,GraduationType
Fill that out to as long as you have the information. The script will automatically delete a graduation on the day of the graduation so it is no longer recorded. On a future release, I hope to simplify the file into just 'YYYY-MM-DD' for simplicity.

After you've done all this, you should just be able to run the script! For further instructions, see [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-create-a-twitterbot-with-python-3-and-the-tweepy-library).
