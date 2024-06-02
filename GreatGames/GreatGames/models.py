from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from GreatGames import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')


class Customer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class Developer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = Developer(user_data)
    print(user)


class Game(ModelMixin):
    def __init__(self, game_data: Dict):
        super(Game, self).__init__(game_data)
        self.pk = game_data.get('pk')
        self.category = game_data.get('genre')
        self.item = game_data.get('title')
        self.unit = game_data.get('rating')
        self.variety = game_data.get('edition')
        self.price = game_data.get('price')
        # From JOIN w/ Sell relation
        self.available = game_data.get('available')
        self.farmer_name = game_data.get('developer_name')
        self.farmer_pk = game_data.get('developer_pk')


class Sell(ModelMixin):
    def __init__(self, sell_data: Dict):
        super(Sell, self).__init__(sell_data)
        self.available = sell_data.get('available')
        self.developer_pk = sell_data.get('developer_pk')
        self.game_pk = sell_data.get('game_pk')


class GameOrder(ModelMixin):
    def __init__(self, game_order_data: Dict):
        super(GameOrder, self).__init__(game_order_data)
        self.pk = game_order_data.get('pk')
        self.customer_pk = game_order_data.get('customer_pk')
        self.developer_pk = game_order_data.get('developer_pk')
        self.game_pk = game_order_data.get('game_pk')
