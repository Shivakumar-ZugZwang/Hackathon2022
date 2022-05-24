from ChessApp import create_app
app,socket = create_app()
# app.run(debug=True,host="0.0.0.0")
socket.run(app,host="0.0.0.0")