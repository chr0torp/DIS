from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from GreatGames.forms import FilterGamesForm, AddGameForm, BuyGameForm, RestockGamesForm
from GreatGames.models import Game as GameModel, GameOrder
from GreatGames.queries import insert_game, get_game_by_pk, Sell, \
    insert_sell, get_all_games_by_developer, get_games_by_filters, insert_game_order, update_sell, \
    get_orders_by_customer_pk

Game = Blueprint('Games', __name__)


@Game.route("/games", methods=['GET', 'POST'])
def game():
    form = FilterGamesForm()
    title = 'Our games!'
    game = []
    if request.method == 'POST':
        game = get_games_by_filters(genre=request.form.get('genre'),
                                         title=request.form.get('title'),
                                         edition=request.form.get('edition'),
                                         developer_name=request.form.get('sold_by'),
                                         price=request.form.get('price'))
        title = f'Our {request.form.get("genre")}!'
    return render_template('pages/games.html', game=game, form=form, title=title)


@Game.route("/add-game", methods=['GET', 'POST'])
@login_required
def add_game():
    form = AddGameForm(data=dict(developer_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            game_data = dict(
                genre=form.genre.data,
                title=form.title.data,
                edition=form.edition.data,
                rating=form.rating.data,
                price=form.price.data
            )
            game = GameModel(game_data)
            new_game_pk = insert_game(game)
            sell = Sell(dict(developer_pk=current_user.pk, game_pk=new_game_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-game.html', form=form)


@Game.route("/your-games", methods=['GET', 'POST'])
@login_required
def your_game():
    form = FilterGamesForm()
    game = []
    if request.method == 'GET':
        game = get_all_games_by_developer(current_user.pk)
    if request.method == 'POST':
        game = get_games_by_filters(genre=request.form.get('genre'),
                                         title=request.form.get('title'),
                                         edition=request.form.get('edition'),
                                         developer_pk=current_user.pk)
    return render_template('pages/your-games.html', form=form, game=game)


@Game.route('/games/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_game(pk):
    form = BuyGameForm()
    game = get_game_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = GameOrder(dict(game_pk=game.pk,
                                      developer_pk=game.developer_pk,
                                      customer_pk=current_user.pk))
            insert_game_order(order)
            update_sell(available=False,
                        game_pk=game.pk,
                        developer_pk=game.farmer_pk)
    return render_template('pages/buy-games.html', form=form, game=game)


@Game.route('/game/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_game(pk):
    form = RestockGamesForm()
    game = get_game_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        game_pk=game.pk,
                        farmer_pk=game.developer_pk)
    return render_template('pages/restock-game.html', form=form, game=game)


@Game.route('/game/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)