# New, much more profitable bot available in return for referral link use:

https://hacks.substack.com/p/huobi-trader-live-now-we-watch



app.py is this strategyy automated:

From the Markets tab (doing this manually) you would click on Leveraged Tokens, click the box that says X3 only and then pull back every % increase on day so far (resets at midnight GMT).  Only BULLSHIT and %BULL/USD are needed 

Maybe there will still be too many to track and we'll need to restrict them to ones showing >5% or less than -5%

Don't spend too long on it - you might quickly find that the data from that page just isn't accessible via api (I suppose scraping might be possible)

All of those tokens start at zero on the left hand side of the graph when the new day begins, then they splay out up or down depending on returns.  You graph only bull/usd (not usdt which would be repetitive), and I'll take the big ups to buy bull tokens and the big downs to buy bears.  Should look like an open fan laid on its side.

Best manual return I got was SXPBULL going from $500 to $5000 in the day, but I regularly see them do 40%.  It's just a matter of spotting the big moves early.

Reset is 1am current UK time which I believe is midnight UTC

Looking good thanks.  Yes, we have to reset at midnight, as they set back to zero for all tokens then.  There might be some value in saving a snapshot before the reset, but I would just use that to give me a feel for how something had acted previously.  My untested observation is that the extreme winners one day are the extreme losers the next.  I can save screenshots manually for now.

So here's the pro tip which will save you half of your data points.  Only plot the %BULL/USD tokens (plus BULLSHIT).  You don't need the BEAR tokens because they are always the opposite result to BULL, give or take.  By looking at the biggest losses on the BULL, I will know to buy a BEAR token.  Does that make sense?


Now, did the FTX token chart go anywhere, or is the info not available in an automated manner?  I would just need a week of monitoring that to be able to suggest a working system based on it (initial observation is that if it goes >10% in the first 3 hours after 1am reset, it's going to be huge).


1. sign up for FTX here (even if you already have an account, support the dev): https://ftx.com/#a=2579313

2. Follow these steps:

git clone https://github.com/DunnCreativeSS/FTX_token_visualizer

cd FTX_token_visualizer

pip install ccxt pytz

export ftxkey=Sm7R0...

export ftxsecret=NiyOA...

export limit=20

python app.py


this should do it (on linux, on windows the 'export' commands are something like setx ftxkey "whatever" then open a new cmd window)
