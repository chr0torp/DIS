from GreatGames import db_cursor, conn
from GreatGames.models import User, Developer, Customer, Game, Sell, GameOrder


# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_developer(developer: Developer):
    sql = """
    INSERT INTO Developers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (developer.user_name, developer.full_name, developer.password))
    conn.commit()


def insert_customer(customer: Customer):
    sql = """
    INSERT INTO Customers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
    conn.commit()


def insert_game(game: Game):
    sql = """
    INSERT INTO Games(genre, title, rating, edition, price)
    VALUES (%s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        Game.genre,
        Game.title,
        Game.rating,
        Game.edition,
        Game.price
    ))
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(developer_pk, game_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.developer_pk, sell.game_pk,))
    conn.commit()


def insert_game_order(order: GameOrder):
    sql = """
    INSERT INTO GameOrder(game_pk, developer_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.game_pk,
        order.developer_pk,
        order.customer_pk,
    ))
    conn.commit()


# SELECT QUERIES
def get_user_by_pk(pk):
    sql = """
    SELECT * FROM Users
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_developer_by_pk(pk):
    sql = """
    SELECT * FROM Developers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    developer = Developer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return developer


def get_games_by_filters(genre=None, title=None, edition=None,
                           developer_pk=None, developer_name=None, price=None):
    sql = """
    SELECT * FROM vw_games 
    WHERE
    """
    conditionals = []
    if genre:
        conditionals.append(f"genre='{genre}'")
    if title:
        conditionals.append(f"title='{title}'")
    if edition:
        conditionals.append(f"edition = '{edition}'")
    if developer_pk:
        conditionals.append(f"developer_pk = '{developer_pk}'")
    if developer_name:
        conditionals.append(f"developer_name LIKE '%{developer_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    games = [Game(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return games


def get_customer_by_pk(pk):
    sql = """
    SELECT * FROM Customers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return customer


def get_game_by_pk(pk):
    sql = """
    SELECT game_pk as pk, * FROM vw_game
    WHERE game_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    games = Game(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return games


def get_all_games_by_developer(pk):
    sql = """
    SELECT * FROM vw_game
    WHERE developer_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    games = [Game(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return games


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_all_games():
    sql = """
    SELECT game_pk as pk, genre, title, edition, rating, price, developer_name, available, developer_pk
    FROM vw_games 
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql)
    games = [Game(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return games


def get_available_games():
    sql = """
    SELECT * FROM vw_produce
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    games = [Game(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return games


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM GameOrder po
    JOIN Game p ON p.pk = po.game_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [GameOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, game_pk, developer_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE game_pk = %s
    AND developer_pk = %s
    """
    db_cursor.execute(sql, (available, game_pk, developer_pk))
    conn.commit()
