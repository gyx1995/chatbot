import respondMsg
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    args = request.args["value"]
    respond = respondMsg.respond(args)
    return "callback" + "(" + "{\"response\":" + "\"" + respond + "\"}" + ")"


if __name__ == "__main__":
    app.run()

