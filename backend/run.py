from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
import pickle

app = Flask(__name__)
api = Api(app)

# Load pipeline and model using the binary files
model = pickle.load(open('model.pkl', 'rb'))

# Function to test if the request contains multiple 
def islist(obj):
  return True if ("list" in str(type(obj))) else False

class Preds(Resource):
  def put(self):
    json_ = request.json
    entry = pd.DataFrame([json_])
    # Transform request data record/s using the pipeline
    # entry_transformed = pipeline.transform(entry)
    # Make predictions using transformed data
    print(json_)
    prediction = model.predict(entry)
    res = {'predictions': {}}

    print(prediction)
    # # Create the response
    # for i in range(len(prediction)):
    #   res['predictions'][i + 1] = int(prediction[i])

    return res, 200 # Send the response object

api.add_resource(Preds, '/predict')

if __name__ == "__main__":
  app.run(debug = True)

# to run the flask app
# export FLASK_APP=run
# flask run