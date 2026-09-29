from datetime import datetime

from flask import Flask, Response, redirect, render_template, request, url_for


app = Flask(__name__, static_folder="static")


ARTICLE_SLUGS = [
    "arbiquant-bewertung",
    "arbiquant-bewertung-analyse",
    "arbiquant-erfahrungen",
    "arbiquant-erfahrungen-2026",
    "arbiquant-erklaert",
    "arbiquant-plattform-ueberblick",
    "arbiquant-serios-oder-betrug",
    "arbiquant-test-2026",
    "arbiquant-trading",
    "arbiquant-was-ist-das",
]


@app.before_request
def redirect_to_https():
    if request.headers.get("X-Forwarded-Proto") == "http":
        return redirect(request.url.replace("http://", "https://", 1), code=301)

    if request.host.startswith("www."):
        new_host = request.host[4:]
        new_url = request.url.replace(f"//www.{new_host}", f"//{new_host}", 1)
        return redirect(new_url, code=301)


@app.route("/index.php")
@app.route("/index.html")
def redirect_index():
    return redirect(url_for("index"), code=301)


@app.errorhandler(404)
def not_found(error):
    return render_template("404/index.html"), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
@app.route("/about/")
def about():
    return render_template("about/index.html")


@app.route("/contact")
@app.route("/contact/")
def contact():
    return render_template("contact/index.html")


@app.route("/terms")
@app.route("/terms/")
def terms():
    return render_template("terms/index.html")


def _register_article_routes():
    for slug in ARTICLE_SLUGS:
        endpoint = f"article_{slug.replace('-', '_')}"

        def make_view(template_slug):
            def view():
                return render_template(f"{template_slug}/index.html")

            return view

        view_func = make_view(slug)
        app.add_url_rule(f"/{slug}", endpoint=endpoint, view_func=view_func)
        app.add_url_rule(f"/{slug}/", endpoint=f"{endpoint}_slash", view_func=view_func)


_register_article_routes()


@app.route("/sitemap.xml")
def sitemap():
    base_url = request.url_root.rstrip("/")
    if request.headers.get("X-Forwarded-Proto") == "https":
        base_url = base_url.replace("http://", "https://")
    lastmod = datetime.utcnow().date().isoformat()

    urls = ["/", "/about/", "/contact/", "/terms/"]
    urls.extend(f"/{slug}/" for slug in ARTICLE_SLUGS)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.extend(
            [
                "    <url>",
                f"        <loc>{(base_url + url).rstrip('/')}</loc>",
                f"        <lastmod>{lastmod}</lastmod>",
                "        <changefreq>monthly</changefreq>",
                "        <priority>0.8</priority>",
                "    </url>",
            ]
        )
    lines.append("</urlset>")
    return Response("\n".join(lines), mimetype="application/xml")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
