from flask import Blueprint, render_template, request, jsonify
from logic.global_alignment import GlobalAlignment

bp = Blueprint('global_alignment_route', __name__)

@bp.route('/N-W', methods=['GET', 'POST'])
def N_W():
    if request.method == 'GET':
        return render_template('global_alignment.html')
    elif request.method == 'POST':
        # Receive sequence data from request
        data = request.get_json()
        seq1 = data['seq1']
        seq2 = data['seq2']
        match_var = data['match']
        mismatch_var = data['mismatch']
        gap_var = data['gap']

        alignments = GlobalAlignment()

        # Perform alignment
        all_alignments, optimal_paths,score, score_matrix, arrows = alignments.needleman_wunsch(seq1, seq2, match_var, mismatch_var, gap_var)
        
        # Return alignment results as JSON
        return jsonify({
            'all_alignments': all_alignments,
            'optimal_paths': optimal_paths,
            'score': score,
            'score_matrix': score_matrix,
            'arrows': arrows
        })
    
@bp.route('/SG-N-W', methods=['POST'])
def SG_N_W():
    if request.method == 'POST':
        # Receive sequence data from request
        data = request.get_json()
        seq1 = data['seq1']
        seq2 = data['seq2']
        match_var = data['match']
        mismatch_var = data['mismatch']
        gap_var = data['gap']

        alignments = GlobalAlignment()

        # Perform alignment
        all_alignments, optimal_paths,score, score_matrix, arrows = alignments.needleman_wunsch_semi_global(seq1, seq2, match_var, mismatch_var, gap_var)
        
        # Return alignment results as JSON
        return jsonify({
            'all_alignments': all_alignments,
            'optimal_paths': optimal_paths,
            'score': score,
            'score_matrix': score_matrix,
            'arrows': arrows
        })