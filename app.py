#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import os
from datetime import timedelta
from typing import List, Dict

from flask import Flask, request, session, render_template, jsonify
from flask.cli import load_dotenv

from agent.agent_with_rag import run_agent

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=['GET'])
def form():
    return render_template('agent.html', history=session.get('history', []))


@app.route('/agent', methods=['POST'])
async def agent():
    session.permanent = True
    user_input = request.form['user-input']
    system_prompt = request.form['system-prompt']
    history: List[Dict[str, str]] = session.get('history', [])
    response = await run_agent(user_input, system_prompt, history)
    if 'history' not in session:
        session['history'] = []
    session['history'].append({'type': 'user', 'message': user_input})
    session['history'].append({'type': 'ai', 'message': response})
    return jsonify(user_input=user_input, response=response)


if __name__ == '__main__':
    app.run()
