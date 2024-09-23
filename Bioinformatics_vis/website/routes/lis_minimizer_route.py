from flask import Blueprint, render_template, request, jsonify
from logic.lis_minimizer import find_minimizers, keep_unique_first_values, find_matching_minimizers, extract_position2_sequence, longest_increasing_subsequences, find_minimizers_by_position2

bp = Blueprint('lis_minimizer_route', __name__)

@bp.route('/LIS', methods=['GET', 'POST'])
def page7():
    if request.method == 'GET':
        return render_template('lis_minimizer.html')
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


        matches = find_matching_minimizers(minimizers_sequence_one,minimizers_sequence_two)

        position2_sequence = extract_position2_sequence(matches)

        lis, lis_steps = longest_increasing_subsequences(position2_sequence)

        minimizers_for_lis = find_minimizers_by_position2(lis, matches)

        return jsonify({
            'minimizers_one': minimizers_sequence_one,
            'minimizers_two': minimizers_sequence_two,
            'matches': matches,
            'lis': lis,
            'minimizers_for_lis': minimizers_for_lis,
            'lis_steps' : lis_steps
        })
