from app import create_app

app = create_app()

if __name__ == "__main__":
	# host=0.0.0.0 permite acceder desde la red local si se requiere
	app.run(host="127.0.0.1", port=5000, debug=True)
