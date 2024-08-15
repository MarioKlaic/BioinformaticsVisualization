from flask import Blueprint, render_template, request, jsonify
from minimizers import find_minimizers, keep_unique_first_values

bp = Blueprint('minimizers_route', __name__)

@bp.route('/minimizers', methods=['GET', 'POST'])
def page8():
    if request.method == 'GET':
        return render_template('minimizers.html')
    elif request.method == 'POST':
        # Receive sequence data from request
        data = request.get_json()
        seq = data['seq']
        k = int(data['k'])
        w = int(data['w'])
        
        # Find minimizers for both sequences

        minimizers, rows = find_minimizers(seq, k, w)
        print(minimizers)
        return jsonify({
            'minimizers': minimizers,
            'rows': rows
        })
