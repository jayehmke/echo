import logging
from random import randint
from flask import Flask, render_template, render_template_string
from flask_ask import Ask, statement, question, session
from flask_mongoengine import MongoEngine
from scripts import is_plural
from models import *

app = Flask(__name__)
ask = Ask(app, "/")
app.config['MONGODB_SETTINGS'] = {
    'db': 'echodb',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def get_user():
    user_object = session.get('user')
    user_id = user_object.get('userId')
    user = None

    try:
        user = User.objects.get(user_id=user_id)
        print(user)
    except Exception as e:
        logging.error(e)
    return user


@ask.launch
def new_game():
    user = get_user()

    if user is not None:
        welcome_msg = render_template('new_launch')

    else:
        room_count = Room.objects.count(owner=user.id)

        if room_count < 1:
            welcome_msg = render_template("launch_no_rooms")
        else:
            welcome_msg = render_template("welcome")

    return question(welcome_msg)


@ask.intent("LocateIntent", convert={'item': str})
def find_item(item):
    print("Locate Intent")

    user = get_user()
    requested_item = None

    try:
        requested_item = Item.objects.get(name=item, owner=user.id)
    except Exception as e:
        logging.error(e)

    print('item', item)
    isp, lemma = is_plural(item)
    print(item, lemma, isp)
    if isp:
        verb = 'are'
    else:
        verb = 'is'
    response = render_template('item_located', item=item, verb=verb)
    return statement(response)


@ask.intent("AssignIntent", convert={'item': str, 'location': str})
def assign_item(item, location):
    print(item, location)

    user = get_user()
    try:
        item = Item.objects.create(name=item, owner=user.id)
        response = render_template_string('I have assigned the {} to the {}'.format(item, location))
    except Exception as e:
        response = render_template_string('There was an error assigning the object. Please try again.')
    return statement(response)


@ask.intent("AddRoomIntent")
def add_room():
    message = render_template("add_room_prompt")
    return question(message)

# @ask.intent("YesIntent")
# def next_round():
#     numbers = [randint(0, 9) for _ in range(3)]
#     round_msg = render_template('round', numbers=numbers)
#     session.attributes['numbers'] = numbers[::-1]  # reverse
#     return question(round_msg)


# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
# def answer(first, second, third):
#     winning_numbers = session.attributes['numbers']
#
#     if [first, second, third] == winning_numbers:
#         msg = render_template('win')
#
#     else:
#         msg = render_template('lose')
#
#     return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)
