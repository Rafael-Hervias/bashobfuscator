from flask import Flask, jsonify, render_template, redirect, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from obf import order

from datetime import datetime
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


@app.route('/static/<path>', methods=['GET'])
def server_static(path):
    return send_from_directory("static", path)


@app.route('/', methods=['GET', 'POST'])
def index():
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'-- Request from {request.remote_addr} at {dt_string} --')
    print(f'- {request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}')
    [print(f'- {x}: {request.headers[x]}') for x in request.headers.keys()]
    print(f'- {request.get_data().decode("utf-8")}')
    print(f'--------------------------------------------------')
    if request.method == 'GET':
        return render_template("home.html")
    elif request.method == 'POST':
        return jsonify("hello post")


@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    output = str(request.json["data"])
    output = order(output)
    return jsonify(output)


@app.route('/github', methods=['GET'])
def redirect_github():
    return redirect("https://github.com/")


@app.route('/aboutme', methods=['GET'])
def redirect_aboutme():
    return redirect("https://google.com/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)

