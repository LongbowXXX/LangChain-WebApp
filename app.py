#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import os

from flask import Flask, request, session, render_template, jsonify
from flask.cli import load_dotenv

from agent.agent_with_rag import run_agent

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET'])
def form():
    return render_template('agent.html', history=session.get('history', []))


@app.route('/agent', methods=['POST'])
async def agent():
    user_input = request.form['user-input']
    system_prompt = request.form['system-prompt']
    response = await run_agent(user_input, system_prompt)
    if 'history' not in session:
        session['history'] = []
    session['history'].append((user_input, response))
    return jsonify(user_input=user_input, response=response)


if __name__ == '__main__':
    app.run()
