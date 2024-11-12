from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/fallback/merchant')  # URL yo'nalishi to'g'ri yozilganligiga ishonch hosil qiling
def redirect_to_custom_scheme():
    # Bu yerda brauzerda JavaScript orqali yo'naltirish yoki oddiy HTML sahifani qaytarish mumkin
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirect Page</title>
    </head>
    <body>
        <h1>Welcome to the Redirect Page</h1>
        <p>If you are not redirected, please check the URL or open our app manually.</p>
    </body>
    </html>
    """)

# if __name__ == '__main__':
#     # app.run(debug=True)  # Debug rejimida ishga tushirish, xatolarni aniqlashda yordam beradi
#     app.run(host='127.0.0.1', port=8001,debug=False)
