from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
import requests


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
  first_name = current_user.fname
  nasa_api_key = current_app.config['NASA_API_KEY']
  nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
  response = requests.get(nasa_url)
  if response.status_code == 200:
     data = response.json()
     image_url = data.get("url", "")
     title = data.get("title", "NASA image of the day")
     description = data.get("Explanation", "No description available")
  else:
     image_url = ""
     title = "Image unavailable"
     description = "NASA API Could not fetch the data at this time."
  return render_template('dashboard.html', first_name=first_name, image_url=image_url, title=title, description=description)
