from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
import pickle

app = Flask(__name__)
api = Api(app)

model = pickle.load(open('model.pkl', 'rb'))

def islist(obj):
  return True if ("list" in str(type(obj))) else False

class Preds(Resource):
  def put(self):
    json_ = request.json
    entry = pd.DataFrame([json_])
    prediction = model.predict(entry)
    res = {'prediction': prediction[0]}
    return res, 200

api.add_resource(Preds, '/predict')

if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=5001)

# to run the flask app (make sure to install Flask)
# export FLASK_APP=run
# flask run

# example request
# curl -XPUT -H "Content-type: application/json" -d '{"day_of_week": 5, "temperature": 47, "temp_feel": 41, "wind_mph": 23.7, "wind_degree": 178, "pressure_mb": 1015, "precipitation_mm": 0, "humidity": 90, "cloudiness": 50, "uv_index": 1, "gust_mph": 13.3, "school_break": 0, "is_holiday": 0, "is_rrr_week": 0, "is_finals_week": 0, "is_student_event": 0, "hour": 18}' 'http://127.0.0.1:5000/predict'