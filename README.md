Discord bot built in Python with discord.py

## Features
- /gamble commands and settings - check current credit count, show leaderboard, or gamble your credits
- Uses PostgreSQL database with async SQLAlchemy and alembic migrations to handle server specific data
- More to come, new features are work in progress

## Installation
1. Create discord bot in discord developers portal, invite it to your server
2. Create `.env` file, add your discord bot token, and ID of the single discord server where bot will live.
3. Run bot with `docker compose up`
4. Run database migrations `docker compose exec bot alembic upgrade head`
