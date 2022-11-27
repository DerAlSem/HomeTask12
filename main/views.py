from flask import Blueprint, render_template, json, request
from json import JSONDecodeError
import logging

main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@main_blueprint.route('/')
def index():
    return render_template("index.html")

@main_blueprint.route('/search')
def search_page():
    s = request.args['s']
    logging.info(f'Поиск по вхождению {s}')
    try:
        with open("posts.json", "r", encoding='utf-8') as jsonFile:
            all_posts = json.load(jsonFile)
        founded_posts = list()
        for post in all_posts:
            if s in post['content']:
                founded_posts.append(post)
        result = render_template("post_list.html", keyword = s, founded_posts = founded_posts)
    except FileNotFoundError:
        logging.error('JSON пропал')
        result = 'Не могу загрузить посты: файл не найден'
    except JSONDecodeError:
        logging.error('Невалидный JSON')
        result = 'Не могу загрузить посты: структура файла нарушена'
    return result