from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from GreatGames.forms import FilterGamesForm, AddGameForm, BuyGameForm, RestockGamesForm
from GreatGames.models import Game as GameModel, GameOrder
from GreatGames.queries import insert_game, get_game_by_pk, Sell, \
    insert_sell, get_all_games_by_developer, get_games_by_filters, insert_game_order, update_sell, \
    get_orders_by_customer_pk, get_customer_by_pk 

Produce = Blueprint('Produce', __name__)


@Produce.route("/produce", methods=['GET', 'POST'])
def produce():
    form = FilterGamesForm()
    title = 'Our games!'
    game = []
    if request.method == 'POST':
        game = get_games_by_filters(genre=request.form.get('category'),
                                         title=request.form.get('item'),
                                         edition=request.form.get('variety'),
                                         developer_name=request.form.get('sold_by'),
                                         price=request.form.get('price'),
                                         description=request.form.get('description'))
        title = f'Our {request.form.get("genre")}!'
    return render_template('pages/produce.html', produce=game, form=form, title=title)


@Produce.route("/add-produce", methods=['GET', 'POST'])
@login_required
def add_produce():
    form = AddGameForm(data=dict(developer_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            game_data = dict(
                genre=form.genre.data,
                title=form.title.data,
                edition=form.edition.data,
                rating=form.rating.data,
                price=form.price.data,
                # description=form.description.data
            )
            game = GameModel(game_data)
            new_game_pk = insert_game(game)
            sell = Sell(dict(developer_pk=current_user.pk, game_pk=new_game_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-produce.html', form=form)


@Produce.route("/your-produce", methods=['GET', 'POST'])
@login_required
def your_produce():
    form = FilterGamesForm()
    game = []
    if request.method == 'GET':
        game = get_all_games_by_developer(current_user.pk)
    if request.method == 'POST':
        game = get_games_by_filters(genre=request.form.get('genre'),
                                         title=request.form.get('title'),
                                         edition=request.form.get('edition'),
                                         developer_pk=current_user.pk)
    return render_template('pages/your-produce.html', form=form, produce=game)


@Produce.route('/produce/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_produce(pk):
    form = BuyGameForm()
    game = get_game_by_pk(pk)
    # current_user = get_customer_by_pk(current_user.pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = GameOrder(dict(game_pk=game.pk,
                                      developer_pk=game.farmer_pk,
                                      customer_pk=current_user.pk))
            insert_game_order(order)
            update_sell(available=False,
                        game_pk=game.pk,
                        developer_pk=game.farmer_pk)
    return render_template('pages/buy-produce.html', form=form, produce=game)


@Produce.route('/produce/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_produce(pk):
    form = RestockGamesForm()
    game = get_game_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        game_pk=game.pk,
                        farmer_pk=game.farmer_pk)
    return render_template('pages/restock-produce.html', form=form, produce=game)


@Produce.route('/produce/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)