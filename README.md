# Does-Icing-the-Kicker-Really-Work?
All NFL fans know the feeling. Your favorite team is playing. It has been a back and forth affair, neither team firmly taking control of the game. It is finally getting down to crunch time. The two minute warning has passed, and the kicker trots on to the field, to attempt a game altering field goal. 

If he is kicking for the opposing team: he looks frail and terrified. How does this guy play the same sport as DK Metcalf and Aaron Donald? 

If he’s kicking for your team: he appears calm and composed. He is going to come through in the clutch once again.

Regardless of which team he is playing for, the scene unfolds predictably. The kicker slows down a few feet behind the long snapper. He methodically takes two long strides backwards, and one wide stride toward his non-kicking foot. Your heart is racing as you yell “Come on! Come on!” at your TV. All of a sudden, the referees blow their whistles and the tension dissipates. The broadcast cuts to the opposing coach on the sideline, pacing nervously. He just called a timeout, hoping to disrupt and ultimately cause the kicker to fail the impending field goal attempt. Typically referred to as “icing the kicker”, this long-employed tactic forces the kicker to expend a few more anxious moments, while sowing doubt and - perhaps - reducing success. 

As a long-time fan of both the NFL and the predictive power of data, I have wondered: does icing the kicker actually cause a statistically significant decrease in the odds of converting the kick? Or, does it only serve as an anti-climactic, time-wasting distraction to serve up even more beer commercials? 




Armed with Python and a trove of historical data, after picking up a few skills along the way, I was finally able to answer this question.

After some research, I found an API (https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId={gameID}) where all I needed to do was plug in an ESPN gameID and it would return a JSON of the play-by-results of the game. My first thought was to run my script on all games since 2001. So I identified the gameID of the first game of the 2001 season (210909012) and the most recent game this season in 2024 (401671696) and planned to run a for-loop in range(210909012,401671696). 

However, I quickly realized that this would require a get-request for nearly 200 million gameIDs. Specifically, I noticed that the get request took up to .5 seconds, meaning that it would take roughly 100 million seconds, or over 3 years, to iterate through this whole range. Knowing that I had to find a way to drastically shorten the list of gameIDs, my next task was to reduce the length of the range that my script would iterate through. 

My initial strategy was to find a discernible pattern in gameIDs, but came up empty. I then consulted with a peer in my Master’s program about this issue, and he suggested using the Beautiful Soup package to scrape the data I needed from HTML. After watching a few YouTube videos and studying related documentation, I was then able to parse through ESPN score page season-by-season and week-by-week, extracting the gameIDs and adding them to a JSON file.

Once all of my data was extracted into a usable form, my next endeavor was to determine which statistical test would be best. Since I had both binary independent and dependent variables, I thought of using a chi-square test of independence. However, I knew I had to account for distance, because it wouldn’t make sense to compare 20 yard field goals with 60 yard field goals. Landing upon the Cochran-Mantel-Haenszel test, which is essentially a chi-square test of independence that accounts for stratification, I knew I found the right tool for the job. I then decided to stratify my data into six yard increments, to ensure that there would be enough data per stratum to perform statistical tests, while also only analyzing comparable distances.

While in the deep end of the data pool, I also calculated the error for both the “iced” bar and “non-iced” bar, but was only able to do so for groups that had both 10 “successes” (converted kicks) and 10 “failures” (missed kicks). Since my dataset was fairly small (n=817) and recognizing that it was divided between 8 groups, for many bars, a margin of error was unable to be calculated. I also assumed a confidence interval of 95%, which corresponds to a z-score of 1.96.



<img width="615" alt="Screenshot 2024-09-19 at 12 12 46 PM" src="https://github.com/user-attachments/assets/5b8c04e3-e19e-4cc7-b168-24f501257d08">




In the end, the Cochran-Mantel-Haenszel calculated a p-value of .1651. This is greater than .05, so we can conclude that there is not a statistically significant effect of “icing” a kicker on converting a field goal attempt.


In retrospect, there certainly were some limitations to this study. One, the aforementioned sample size was small, to the point that not all necessary statistical tests could be applied. Two, there are tons of other variables at play: the quality of the kicker, wind, temperature, score of the game, when the “icing” timeout occurred (e.g. when the kicker initially enters the field, as the teams get to the line of scrimmage, after the kicker takes his strides backwards and sideways, etc.), and whether or not it is a postseason game. Perhaps I can make a logistic regression with all of these factors at some point and see which of them are actually the most impactful.




Will we continue to see coaches “ice” kickers? Yes, for the time being. No NFL coach cares what a 22 year old nerd has to say. Besides, there’s plenty of beer to sell until I can get them to listen.



