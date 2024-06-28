from flask import Blueprint, request, jsonify, render_template
from sa_is import SAIS

bp = Blueprint('sa_is_route', __name__)

@bp.route('/SA-IS')
def page3():
    return render_template('sa-is.html')

@bp.route('/sais.py', methods=['POST'])
def sa_is():
    text = request.json.get('text')
    sa_is = SAIS()
    sa = sa_is.makeSuffixArrayByInducedSorting(text.encode('utf-8'), 256)
    
    sa_is.showSuffixArray(sa)
    if sa is not None:
        steps = sa_is.getSteps()
    else:
        print("nothing found error")
    return jsonify(steps_table=steps)
