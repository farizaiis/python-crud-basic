import connexion

options = {"swagger_ui": True}
app = connexion.App(__name__, specification_dir="./", options=options)

app.add_api("swagger.yml")


@app.route('/')
def home():
    return "Server Running"

if __name__ == "__main__":
    app.run(threaded=True, debug=True)