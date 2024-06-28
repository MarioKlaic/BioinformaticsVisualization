from flask import Flask, render_template
from .routes.fm_route import bp as fm_route
from .routes.global_alignment_route import bp as global_alignment_route
from .routes.suffix_tree_route import bp as suffix_tree_route
from .routes.sa_is_route import bp as sa_is_route
from .routes.lcs_minimizer_route import bp as lcs_minimizer_route
from .routes.lis_minimizer_route import bp as lis_minimizer_route

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

    @app.route('/')
    def index():
        return render_template('index.html')

    # Return the created app
    return app
