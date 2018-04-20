from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from cooker import cooker
from cooker import db
from cooker.forms import LoginForm, RegistrationForm, DeckForm
from cooker.models import *
import pdb


def add_to_deck(deck, card, c):
    new = True
    if card.types[0] == 'Creature':
        key = str(card.pk)
        if deck.creatures.get(key):
            new = False
            deck.creatures[key][1] += c
        else:
            deck.creatures[key] = [card, c]
        deck.save()
        return [deck.creatures[key][1], new]
    elif card.types[0] == 'Instant':
        key = str(card.pk)
        if deck.instants.get(key):
            new = False
            deck.instants[key][1] += c
        else:
            deck.instants[key] = [card, c]
        deck.save()
        return [deck.instants[key][1], new]
    elif card.types[0] == 'Sorcery':
        key = str(card.pk)
        if deck.sorceries.get(key):
            new = False
            deck.sorceries[key][1] += c
        else:
            deck.sorceries[key] = [card, c]
        deck.save()
        return [deck.sorceries[key][1], new]
    elif card.types[0] == 'Artifact':
        key = str(card.pk)
        if deck.artifacts.get(key):
            new = False
            deck.artifacts[key][1] += c
        else:
            deck.artifacts[key] = [card, c]
        deck.save()
        return [deck.artifacts[key][1], new]
    elif card.types[0] == 'Enchantment':
        key = str(card.pk)
        if deck.enchantments.get(key):
            new = False
            deck.enchantments[key][1] += c
        else:
            deck.enchantments[key] = [card, c]
        deck.save()
        return [deck.enchantments[key][1], new]
    elif card.types[0] == 'Land':
        key = str(card.pk)
        if deck.lands.get(key):
            new = False
            deck.lands[key][1] += c
        else:
            deck.lands[key] = [card, c]
        deck.save()
        return [deck.lands[key][1], new]
    elif card.types[0] == 'Planeswalker':
        key = str(card.pk)
        if deck.planeswalkers.get(key):
            new = False
            deck.planeswalkers[key][1] += c
        else:
            deck.planeswalkers[key] = [card, c]
        deck.save()
        return [deck.planeswalkers[key][1], new]

@cooker.route('/')
@cooker.route('/index')
def index():
    return render_template('index.html', title='Home')

@cooker.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@cooker.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@cooker.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.save()
        flash('Welcome!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@cooker.route('/user/<username>')
@login_required
def user(username):
    user = User.objects(username=username).first_or_404()
    return render_template('user.html', user=user)

@cooker.route('/user/<username>/decks')
def decks(username):
    user = User.objects(username=username).first_or_404()
    decks = Deck.objects(author=user)
    return render_template('decks.html', user=user, decks=decks)

@cooker.route('/add_deck', methods=['GET', 'POST'])
@login_required
def add_deck():
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck()
        if form.deck_type.data == 'Commander':
            deck = Commander()
        elif form.deck_type.data == 'Legacy':
            deck = Legacy()
        elif form.deck_type.data == 'Vintage':
            deck = Vintage()
        elif form.deck_type.data =='Modern':
            deck = Modern()
        deck.name = form.name.data
        deck.author = current_user.pk
        deck.description = form.description.data
        deck.save()
        flash('Deck Created!')
        return redirect(url_for('decks', username=current_user.username))
    return render_template('add_deck.html', title='Add Deck', form=form)

@cooker.route('/user/<username>/deck/<dpk>', methods=['GET', 'POST'])
def deck_detail(username, dpk):
    user = User.objects(username=username).first_or_404()
    deck = Deck.objects(pk=dpk).first_or_404()
    if not deck.author == user:
        abort(404)
    return render_template('deck_detail.html', title='Deck Detail', user=user, deck=deck)


@cooker.route('/add_card', methods=['POST'])
@login_required
def add_card():
    deck = Deck.objects(pk=request.form['dpk']).first_or_404()
    card = Card.objects(name=request.form['card_name']).first_or_404()
    count = 0
    try:
        count = add_to_deck(deck, card, int(request.form['card_count']))
    except:
        count = add_to_deck(deck, card, 1)
    return jsonify({'name': card.name,
                    'count': count[0],
                    'type': "#"+card.types[0],
                    'countid': 'count_'+str(card.pk),
                    'rowid': 'row_'+str(card.pk),
                    'key': str(card.pk),
                    't': card.types[0],
                    'new': count[1]})

@cooker.route('/remove_card', methods=['POST'])
@login_required
def remove_card():
    deck = Deck.objects(pk=request.form['dpk']).first_or_404()
    if request.form['ctype'] == 'Creature':
        del deck.creatures[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Instant':
        del deck.instants[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Sorcery':
        del deck.sorceries[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Artifact':
        del deck.artifacts[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Enchantment':
        del deck.enchantments[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Land':
        del deck.lands[request.form['cpk']]
        deck.save()
    if request.form['ctype'] == 'Planeswalker':
        del deck.planeswalkers[request.form['cpk']]
        deck.save()
    return jsonify({'row': '#row_'+request.form['cpk']})


@cooker.route('/card_autocomplete')
def card_autocomplete():
    results = []
    search = request.args.get('q')
    if search:
        results.append(Card.objects(name__istartswith=search).distinct('name')[0:9])
    return jsonify(results)
