from flask import render_template


def page_not_found(e):
    """
    Page not found a.k.a 404 controller.
    """
    return render_template("404.html"), 404
