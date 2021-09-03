import os
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# get files sort by datetime
def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    a.reverse()

    return a

# replace template
def get_template_content(template_file):
    file_path = os.path.join(os.getcwd() + "/templates/" + template_file)
    file_content = ""

    with open(file_path) as f:
        file_content = f.read()
        f.close()

    return file_content

@app.route("/version")
def figure_version_viwer():
    # version
    version_num = request.args.get("number")

    # static image directory
    image_directory = os.getcwd() + "/static/images/"

    # prepare directory content
    directory_content = ""
    for file in getfiles(image_directory):
        file_path = os.path.join(image_directory, file)
        if not os.path.isfile(file_path) and file.isdigit():
            modify_time_since_epoc = os.stat(file_path).st_ctime
            last_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modify_time_since_epoc))
            if int(file) == int(version_num):
                directory_content = directory_content + "<div class=\"selected\"><p class=\"ex5\"><a href=\"/version?number={0}\">#{1} - {2}</a></p></div>".format(int(file), file, last_modify_time)
            else: 
                directory_content = directory_content + "<p class=\"ex5\"><a href=\"/version?number={0}\">#{1} - {2}</a></p>".format(int(file), file, last_modify_time)

    # prepare figure content
    figure_content = ""
    version_path = "/static/images/{0}".format(version_num)
    for file in getfiles(os.getcwd() + version_path):
        if file.endswith(".gif"):
            pure_name = os.path.splitext(file)[0]
            gif_name = pure_name + ".gif"
            mp4_name = pure_name + ".mp4"
            xml_name = pure_name + ".xml"
            figure_content = figure_content + "<p class=\"ex2\"> File : {1} [<a href=\"{0}/{2}\" target=\"_blank\">Gif</a>, <a href=\"{0}/{3}\" target=\"_blank\">Mp4</a>, <a href=\"{0}/{4}\" target=\"_blank\">Xml</a>]</p>".format(version_path, pure_name, gif_name, mp4_name, xml_name)
            figure_content = figure_content + "<p class=\"ex5\"><img src=\"{0}/{1}\" ></p>".format(version_path, file)


    html_content = get_template_content('index.html')
    html_content = html_content.replace("{LEFT_CONTENT}", figure_content)
    html_content = html_content.replace("{RIGHT_CONTENT}", directory_content)

    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)