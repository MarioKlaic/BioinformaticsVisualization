import pickle
from flask import Blueprint, render_template, request, jsonify, session
from logic.suffix_tree import SuffixTree

bp = Blueprint('suffix_tree_route', __name__)

@bp.route('/suffix_tree', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        text = request.json.get('text')
        suffix_tree = SuffixTree(text)
        #suffix_tree.build_tree()
        tree_structure = suffix_tree.get_tree_structure_and_links()
        session['suffix_tree'] = pickle.dumps(suffix_tree)
        return jsonify(tree_structure=tree_structure)
    else:
        return render_template('suffix_tree.html')

@bp.route('/suffix_tree_next', methods=['POST'])
def suffix_tree_next():
    suffix_tree_serialized = session.get('suffix_tree')
    if suffix_tree_serialized is not None:
        if request.method == 'POST':
            step = request.json.get('step') - 1
            suffix_tree = pickle.loads(suffix_tree_serialized)
            text = suffix_tree.text
            suffix_tree.add_char(text[step])
            tree_structure = suffix_tree.get_tree_structure_and_links() #expanded to return suffixes aswell

            session['suffix_tree'] = pickle.dumps(suffix_tree)
            suffixes = suffix_tree.get_suffixes(tree_structure, text)      
            return jsonify(tree_structure=tree_structure, suffixes=suffixes)
        else:
            return render_template('suffix_tree.html')
    else:
        print("nothing found, error")
