from flask import Flask, render_template, jsonify, send_from_directory, abort
import os
import json
from .routes.fm_route import bp as fm_route
from .routes.global_alignment_route import bp as global_alignment_route
from .routes.suffix_tree_route import bp as suffix_tree_route
from .routes.sa_is_route import bp as sa_is_route
from .routes.lcs_minimizer_route import bp as lcs_minimizer_route
from .routes.lis_minimizer_route import bp as lis_minimizer_route
from .routes.minimizers_route import bp as minimizers_route


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'secretlyHidden'

    # Register blueprints
    app.register_blueprint(fm_route)
    app.register_blueprint(suffix_tree_route)
    app.register_blueprint(sa_is_route)
    app.register_blueprint(global_alignment_route)
    app.register_blueprint(lcs_minimizer_route)
    app.register_blueprint(lis_minimizer_route)
    app.register_blueprint(minimizers_route)
    

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/<lang>.json')
    def language(lang):
        file_path = os.path.join('website', 'static', 'localization', f'{lang}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            return jsonify(data)
        else:
            abort(404, description="Language file not found")

    # Return the created app
    return app
