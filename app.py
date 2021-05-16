import pandas as pd
from flask import Flask, render_template
from b import create_df

df = create_df()

    
app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():

  return 'ok'

@app.route('/my-link2/')
def my_link2():

  return str(df.price.iloc[0])

if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)
  #create_order()
  