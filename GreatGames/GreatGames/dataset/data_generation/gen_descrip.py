# Used to generate video game descriptions for the dataset. Descriptions
# are written by ChatGPT. Output file is read by gen_data.py to populate
# the dataset. 

import random

genres = ["Action", "Adventure", "RPG", "Simulation", "Strategy", "Sports"
          , "Puzzle", "MMORPG", "JRPG", "Fighting", "Horror", "Survival"]

base_descriptions = [
    "Experience the excitement in this {genre} game, where {element1} and {element2}.",
    "Dive into the world of {genre} with {element1}, offering {element2}.",
    "This {genre} game provides {element1}, perfect for those who {element2}.",
    "A thrilling {genre} game featuring {element1} and {element2}.",
    "Explore the {genre} genre with {element1}, making it {element2}.",
    "An innovative {genre} game that {element1} and {element2}.",
    "Immerse yourself in this {genre} game, where {element1} meets {element2}.",
    "Embark on an epic {genre} journey where {element1} and {element2} come together.",
    "Unleash your potential in this {genre} game, featuring {element1} and {element2}.",
    "A captivating {genre} experience that blends {element1} with {element2}.",
    "Join the adventure in this {genre} game, where {element1} is paired with {element2}.",
    "This {genre} game offers {element1}, combined with {element2} for endless excitement.",
    "Step into the world of {genre} with {element1} and {element2} at your fingertips.",
    "Challenge yourself in this {genre} game with {element1} and {element2}.",
    "An engaging {genre} game that brings {element1} and {element2} to life.",
    "Discover the thrill of {genre} through {element1} and {element2}.",
    "Immerse yourself in a {genre} game that offers {element1} and {element2}.",
    "Experience a new level of {genre} with {element1} and {element2}.",
    "A {genre} game where {element1} meets {element2} for an unforgettable experience.",
    "Adventure awaits in this {genre} game featuring {element1} and {element2}.",
    "Explore the depths of {genre} with {element1} and {element2} as your guide.",
    "A dynamic {genre} game that integrates {element1} and {element2} seamlessly.",
    "Prepare for an intense {genre} experience with {element1} and {element2}.",
    "This {genre} game captivates with {element1} and {element2} at its core.",
    "Engage in a {genre} adventure where {element1} and {element2} prevail.",
    "A unique {genre} game that offers {element1} alongside {element2}.",
    "Dive into {genre}\ with {element1} and {element2} for a complete experience.",
]

elements1 = [
    "intense battles", "strategic thinking", "puzzle-solving", "high-speed racing",
    "complex narratives", "city-building", "sports management", "character customization"
]

elements2 = [
    "unmatched gameplay", "breathtaking visuals", "endless fun", "challenging levels",
    "immersive soundtracks", "multiplayer options", "realistic physics", "dynamic environments"
]

descriptions = []

for i in range(10000):
    genre = random.choice(genres)
    base_description = random.choice(base_descriptions)
    element1 = random.choice(elements1)
    element2 = random.choice(elements2)
    age_restriction = f"Age Restriction: {random.randint(3, 18)}."
    description = base_description.format(genre=genre, element1=element1, element2=element2)
    full_description = f"{description} {age_restriction}"
    descriptions.append(full_description)

# Save descriptions to a file
with open('descriptions.txt', 'w') as file:
    for description in descriptions:
        file.write(description + '\n')

print("Descriptions saved to 'descriptions.txt'")
