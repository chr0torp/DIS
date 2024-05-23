import os
import pandas as pd

# Added system path to enabling execution with Python.
import sys
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_path)
# sys.path.insert(0, r'C:\Users\Lindholm\Dropbox\DIS\Project main\DIS\GreatGames')

from GreatGames import app

DATASET_PATH = os.path.join(app.root_path, 'dataset', 'games.csv')

def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


df = pd.read_csv(DATASET_PATH, sep=',')

GameGenreChoices = ModelChoices(df.genre.unique())
GameTitleChoices = ModelChoices(df.title.unique())
GameEditionChoices = ModelChoices(df.edition.unique())
# GameRatingChoices = ModelChoices(df.rating.unique())

UserTypeChoices = ModelChoices(['Developer', 'Customer'])

if __name__ == '__main__':
    print(df.title.unique())
    print(GameTitleChoices.choices())
