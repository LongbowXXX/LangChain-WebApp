#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

from flask import Flask, request, session, render_template
from flask.cli import load_dotenv

from agent.agent_with_rag import run_agent

# .flaskenvファイルの内容を読み込見込む
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your secret key'  # セッションを使用するためには秘密鍵が必要です


@app.route('/', methods=['GET', 'POST'])
async def agent():
    if request.method == 'POST':
        user_input = request.form['query']
        response = await run_agent(user_input)
        # ユーザーの入力とその応答をセッションに追加します
        if 'history' not in session:
            session['history'] = []
        session['history'].append((user_input, response))
    return render_template('agent.html', history=session.get('history', []))


if __name__ == '__main__':
    app.run()
