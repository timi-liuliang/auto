import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def figure_main_viwer():
    figure_content = "<!DOCTYPE html>"

    for file in os.listdir(os.getcwd() + "/static/images/"):
        if file.endswith(".gif"):
            figure_content = figure_content + "<p><img src=\"/static/images/{0}\" ></p>".format(file)

    return figure_content

if __name__ == '__main__':
    app.run(debug=True)