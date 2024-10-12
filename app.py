from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        api_key = '00c349a9198a31e4fd151b1e64914bbd'  # Votre clé API
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description']
            }
            return render_template('result.html', weather=weather_data)
        else:
            return render_template('index.html', error="Ville non trouvée.")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

