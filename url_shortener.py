from app import create_app

app = create_app('config.toml')
app.run(debug=True)