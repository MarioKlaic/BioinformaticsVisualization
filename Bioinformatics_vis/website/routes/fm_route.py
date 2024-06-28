from flask import Blueprint, render_template, request, jsonify
from fm_index import FM_INDEX

bp = Blueprint('fm_route', __name__)

@bp.route('/FM_index', methods=['GET', 'POST'])
def page1():
    message = ''
    count = None
    text = ''  # Initialize the text variable
    pattern = ''  # Initialize the pattern variable
    bwt_matrix = None
    rankAll = None
    if request.method == 'POST':
        text = request.form.get('text')  # The original text
        pattern = request.form.get('pattern')  # The pattern to search for
        if text and pattern:
            fm_index = FM_INDEX(text)
            count = fm_index.countMatches2(pattern)
            message = f'The pattern "{pattern}" occurs {count} time(s) in the text.'
            bwt_matrix = fm_index.bwtMatrix()
            rankAll, tots = fm_index.rankAllBwt(fm_index.bw)
            print(bwt_matrix)
        else:
            message = 'Please provide both text and a pattern to search for.'
    return render_template('fm.html', message=message, count=count, text=text, pattern=pattern, bwt_matrix=bwt_matrix, rankAll=rankAll)
