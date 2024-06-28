from flask import Blueprint, render_template, request, jsonify
from lcs_minimizer import find_minimizers, keep_unique_first_values, lcs_table, find_optimal_path

bp = Blueprint('lcs_minimizer_route', __name__)

@bp.route('/LCS', methods=['GET', 'POST'])
def page6():
    if request.method == 'GET':
        return render_template('lcs_minimizer.html')
    elif request.method == 'POST':
        # Receive sequence data from request
        data = request.get_json()
        seq1 = data['seq1']
        seq2 = data['seq2']
        k = int(data['k'])
        w = int(data['w'])
        
        # Find minimizers for both sequences
        minimizers_one = find_minimizers(seq1, k, w)
        minimizers_sequence_one = keep_unique_first_values(minimizers_one)
        minimizers_two = find_minimizers(seq2, k, w)
        minimizers_sequence_two = keep_unique_first_values(minimizers_two)
        
        # Compute LCS table
        table, arrows = lcs_table(minimizers_sequence_two, minimizers_sequence_one)
        optimal_path = find_optimal_path(arrows)
        
        # Return LCS results as JSON
        return jsonify({
            'minimizers_one': minimizers_sequence_one,
            'minimizers_two': minimizers_sequence_two,
            'lcs_table': table,
            'arrows': arrows,
            'optimal_path': optimal_path
        })
