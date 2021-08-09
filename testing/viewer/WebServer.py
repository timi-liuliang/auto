import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def figure_main_viwer():
    figure_content = "<!DOCTYPE html>"
    figure_content = figure_content + "<html><head><style>p.ex1 {margin-left : 5% } </style></head><body>"

    for file in os.listdir(os.getcwd() + "/static/images/"):
        if file.endswith(".gif"):
            figure_content = figure_content + "<p class=\"ex1\"><img src=\"/static/images/{0}\" ></p>".format(file)

    figure_content = figure_content + "</body></html>"

    return figure_content

if __name__ == '__main__':
    app.run(debug=True)