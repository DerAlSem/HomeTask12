from flask import Blueprint, render_template, json, request
import logging


loader_blueprint = Blueprint(
    'loader_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@loader_blueprint.route("/post_form", methods=["GET", "POST"])
def page_post_form():
    return render_template("post_form.html")


@loader_blueprint.route("/post_uploaded", methods=["POST"])
def page_post_upload():
    # получаем и сохраняем картинку
    picture = request.files.get("picture")
    filename = picture.filename
    if is_picture(filename):
        try:
            picture.save(f"./uploads/{filename}")
            # получаем описание картинки
            content = request.values.get("content")
            # обновляем джсон с постами
            update_posts_json(filename, content)
            result = render_template("post_uploaded.html", picture=filename, content=content)
        except FileNotFoundError:
            result = "Ошибка загрузки файла"
            logging.error("Загружаемый файл не загружается, хотя это странно, конечно.")
    else:
        result = "Пожалуйста, загрузите картинку."
        logging.info("Загружаемый файл не картинка, мамай клянуса!")
    return result


@loader_blueprint.errorhandler(413)
def page_not_found(e):
    return "<h1>Размер файла > 2 МБ</h1><p>У нас тут не безлимитный Яндекс Диск!</p>", 413


def update_posts_json(filename, content):
    new_post = {'pic': f"/uploads/{filename}", 'content': content}

    with open("posts.json", "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    data.append(new_post)

    with open("posts.json", "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)


def is_picture(filename):
    extension = filename.split(".")[-1]
    if extension in ['jpg', 'gif', 'png', 'jpeg']:
        return True
    return False
