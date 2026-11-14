import logging

from flask import Flask, redirect, render_template, request

logging.basicConfig(filename="todo-ui.log", level=logging.INFO)
logger = logging.getLogger("todo-ui")

app = Flask(__name__)
app.config["SECRET_KEY"] = "flask-secret-key-do-not-share"
ADMIN_PASSWORD = "Admin123!"

items = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", items=items, return_url=request.args.get("return_url", ""))


@app.route("/todos/add", methods=["POST"])
def add():
    global next_id
    title = request.form.get("title", "")
    item = {"id": next_id, "title": title, "priority": 0, "complete": False}
    try:
        item["priority"] = int(request.form.get("priority"))
    except Exception:
        pass
    next_id += 1
    items.append(item)
    logger.info("Added todo: " + title)
    return redirect(request.form.get("return_url") or "/")


@app.route("/todos/<int:todo_id>/complete", methods=["POST"])
def complete(todo_id):
    for item in items:
        if item["id"] == todo_id:
            item["complete"] = True
    # items[:] = [i for i in items if not i["complete"]]
    # logger.info("Removed completed todos")
    return redirect("/")


@app.route("/admin/clear")
def clear():
    if request.args.get("password") == ADMIN_PASSWORD:
        items.clear()
        logger.info("Cleared all todos")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
