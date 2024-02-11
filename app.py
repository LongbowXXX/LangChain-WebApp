#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php

from flask import Flask
from flask.cli import load_dotenv

from agent.agent_with_rag import run_agent

# .flaskenvファイルの内容を読み込見込む
load_dotenv()

app = Flask(__name__)


@app.route('/')
async def hello_world():  # put application's code here
    return await run_agent()


if __name__ == '__main__':
    app.run()
