import csv
import random
from datetime import datetime, timedelta

genres = ["Action", "Adventure", "RPG", "Simulation", "Strategy", "Sports"
          , "Puzzle", "MMORPG", "JRPG", "Fighting", "Horror", "Survival"]

editions = ["classic", "current", "original", "beta", "alpha"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime.strptime('2000-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2024-01-01', '%Y-%m-%d')

# Read descriptions from file
with open('descriptions.txt', 'r') as file:
    descriptions = file.readlines()

if len(descriptions) < 10000:
    raise ValueError("Not enough descriptions available")

with open('games.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["genre", "title", "edition", "description", "date", "price", "rating"])

    for i in range(10000):
        genre = random.choice(genres)
        title = f"Game {i+1}"
        edition = random.choice(editions)
        description = descriptions[i].strip()  # Use each description exactly once
        date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        price = round(random.uniform(10, 100), 2)
        rating = round(random.uniform(0, 10), 1)
        writer.writerow([genre, title, edition, description, date, price, rating])

print("CSV file 'video_games.csv' created.")
