from flask import Flask, request, render_template, send_from_directory, json
from main.views import main_blueprint
from loader.views import loader_blueprint

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint, url_prefix='/loader')


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


app.run()
