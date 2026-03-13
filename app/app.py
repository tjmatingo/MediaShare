from fastapi import FastAPI, HTTPException


app = FastAPI()

text_posts = {
    1: {
        "title": "Code & Skate High",
        "content": "Just nailed a Python scraper in 30 mins, then hit the skate park for ollies. Coding fuels my flow state—automation by day, shredding by night! 🛼💻 #CodingFun #SkateLife"
    },
    2: {
        "title": "UV vs Pip Win",
        "content": "Switched to UV for installs—blazing fast! Feels like landing a clean kickflip. Who knew package management could be this hype? Loving this coder-skater life. 🚀🛹"
    },
    3: {
        "title": "Scraping + Shredding",
        "content": "Built a Django scraper today that grabs Fiverr gigs effortlessly. Reward? Sunset skate session. Coding's my jam, skating's my high—pure bliss! 🕸️🛼 #PythonLove"
    },
    4: {
        "title": "AI Flow State",
        "content": "Whipped up an AI prompt generator in Python, then grinded rails at the park. When code clicks like a perfect heelflip, nothing beats it! 🤖🏄‍♂️ #AICodingFun"
    },
    5: {
        "title": "React Rips",
        "content": "Frontend React app deployed—smooth as butter. Skated 5km after, wind in my hair. Coding adventures + skate vibes = unbeatable combo! ⚛️🛹 #WebDevJoy"
    },
    6: {
        "title": "Automation Adrenaline",
        "content": "Automated a client's data pipeline—zero bugs! Celebrated with back-to-back 360 flips. Python makes work fun, skating makes life epic. 💨🔄 #FreelanceFun"
    },
    7: {
        "title": "Cyber Skate Dreams",
        "content": "Diving into cybersecurity scripts while dreaming of skate lines. Code secures the net, skates secure my soul. Loving every hack and trick! 🔒🛼 #CodeAndSkate"
    },
    8: {
        "title": "Fiverr Flow",
        "content": "Landed a scraping gig on Fiverr—script done in hours. Hit the ramps for flips. Freelance coding + skating = my perfect hustle! 💼🛹 #GigLife"
    },
    9: {
        "title": "Python Park Vibes",
        "content": "Wrote a WhatsApp API bot, then skated under Harare lights. Coding's creative rush rivals the best skate session. Who's with me? 📱🛼 #PythonFun"
    },
    10: {
        "title": "Bug Hunt High",
        "content": "Squashed a nasty React bug, felt like popping a varial. Debugging's thrilling, skating's freeing—coder's paradise! 🐛🏞️ #DevJoy"
    },
    11: {
        "title": "Webhook Wins",
        "content": "Integrated webhooks for a client—flawless. Reward: skate sesh with mates. Automation magic + board tricks = weekend win! 🔗🛹"
    },
    12: {
        "title": "Skateboard Syntax",
        "content": "Python syntax feels as natural as skating transitions. Just scripted an AI scraper—now off to ollie curbs. Life's too fun! 🐍🛼 #CodingHigh"
    },
    13: {
        "title": "Django Drop-Ins",
        "content": "Dropped a full Django backend today. Skated drop-ins after—both give that stomach-drop thrill. Dev life rocks! 🌐🏄"
    },
    14: {
        "title": "Freelance Flips",
        "content": "Closed two Fiverr automation gigs. Flipped into a skate ramp sesh. Turning code into cash and tricks—pure joy! 💰🛹 #SkaterCoder"
    },
    15: {
        "title": "AI Axel Jumps",
        "content": "Built an AI model that predicts skate spots. Coding + skating fantasies coming true. Who's hyped?! 🤖⛸️ #AIFun"
    },
    16: {
        "title": "Pipeless Paradise",
        "content": "Ditched pip for UV—installs fly! Like skating sans wheels friction. Speed in code, speed on board. Loving it! ⚡🛼"
    },
    17: {
        "title": "Scraping Switcheroo",
        "content": "Switch-stance scraping script: grabs data from anywhere. Switched to fakie skating after. Balance in code and tricks! 🔄🛹"
    },
    18: {
        "title": "React Rampage",
        "content": "React components rendering ramps in my mind. Built a client app, then rampaged the park. Frontend fun forever! ⚛️🏞️"
    },
    19: {
        "title": "Bot Board Tricks",
        "content": "Coded a trading bot—profits incoming. Board tricks for the win. Python pays, skating plays! 🤖🛹 #AutomationFun"
    },
    20: {
        "title": "Cyber Grind",
        "content": "Grinding cybersecurity challenges like skate grinds. Secure code, sick lines—coder-skater duality! 🔒🛼 #CyberFun"
    },
    21: {
        "title": "API Airtime",
        "content": "API integrations giving me airtime vibes. Deployed for a gig, then soared on my board. Elevated life! 🌐✈️"
    },
    22: {
        "title": "Python Pop",
        "content": "Python pop-up scraper: instant data. Popped some ollies after. Explosive fun in code and concrete! 🐍💥"
    },
    23: {
        "title": "Fiverr Fakies",
        "content": "Fiverr proposal accepted—script incoming. Fakie skated home. Reversing gigs into glory! 💼🛹 #FreelanceHigh"
    },
    24: {
        "title": "Skate Script Magic",
        "content": "Scripted a full-stack app. Skated magic lines at dusk. When hobbies sync, everything's golden! 🛼💻"
    },
    25: {
        "title": "Coder's Cruise",
        "content": "Cruised through a Python course module, cruised the skate park. Smooth code, smooth rides—living the dream! 🛹🐍 #LoveCoding"
    }
}


# creating endpoint
# limit is a query parameter
# query parameter = None makes it optional
# add type to allow for fastapi to auto document the execution of the query
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit: 
        return list(text_posts.values())[:limit]
    return text_posts

# endpoint for specific to id Post
@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return text_posts.get(id)