import pandas as pd
from flask import jsonify
from flask import Flask, request, render_template

df20_O = pd.read_csv('2020O.csv')
df20_D = pd.read_csv('2020D.csv')
df19_O = pd.read_csv('2019O.csv')
df19_D = pd.read_csv('2019D.csv')

df20_O.Tm = df20_O.Tm.str.lower()
df20_D.Tm = df20_D.Tm.str.lower()
df19_O.Tm = df19_O.Tm.str.lower()
df19_D.Tm = df20_D.Tm.str.lower()

df19D = df19_D[['Tm', 'Cmp%', 'Int%', 'Sk%', 'Rate']]
df20D = df20_D[['Tm', 'Cmp%', 'Int%', 'Sk%', 'Rate']]

df19D = df19D.drop(df19D.index[[25]])
df20D = df20D.drop(df20D.index[[25]])

df19D['Cmp%'] = pd.to_numeric(df19D['Cmp%'], downcast="float")
df19D['Int%'] = pd.to_numeric(df19D['Int%'], downcast="float")
df19D['Sk%'] = pd.to_numeric(df19D['Sk%'], downcast="float")

df20D['Cmp%'] = pd.to_numeric(df20D['Cmp%'], downcast="float")
df20D['Int%'] = pd.to_numeric(df20D['Int%'], downcast="float")
df20D['Sk%'] = pd.to_numeric(df20D['Sk%'], downcast="float")

df19D['Missed_Stops%'] = -(-0.33*df19D['Cmp%'] + df19D['Int%'] + 0.83*df19D['Sk%'])
df20D['Missed_Stops%'] = -(-0.33*df20D['Cmp%'] + df20D['Int%'] + 0.83*df20D['Sk%'])

df1 = pd.concat([df19D, df20D], axis=0)
df1.columns = ['Tm', 'Cmp%', "Int Rate", "Sack Rate", "QB Rating", "Missed_Stops%"]

df19O = df19_O[['Player','Cmp','Att','Int','Sk','1D','Yds', 'QBR' ]]
df20O = df20_O[['Player','Cmp','Att','Int','Sk','1D','Yds', 'QBR' ]]

df19O['EYards'] = (df19O['Cmp']*df19O['Yds'])/(df19O['Att'] + df19O['Int'] + df19O['Sk']-df19O['1D'])
df20O['EYards'] = (df20O['Cmp']*df20O['Yds'])/(df20O['Att'] + df20O['Int'] + df20O['Sk']-df20O['1D'])

df19O['Yards_diff'] = df19O['Yds']-df19O['EYards']
df20O['Yards_diff'] = df20O['Yds']-df20O['EYards']

df2 = pd.concat([df19O, df20O], axis=0)

df2['Player'] = df2['Player'].str.replace('*', '')
df2['Player'] = df2['Player'].str.replace('+', '')
df2['Player'] = df2['Player'].str.lower()
df2.columns = ['Player', 'Cmp%', 'Pass Att', 'Int', 'Sacks', 'First Downs', 'Yds', 'QB Rating', 'Efficient Yards', 'Efficient Yards over Average']
    
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/d', methods=['POST','GET'])
def my_form_post():
    text = request.form['text']
    processed_text = text.lower()
    return jsonify(df1[df1.Tm == processed_text].to_dict(orient='records')) 

@app.route('/q', methods=['POST', 'Get'])
def my_form_post2():
    text = request.form['qb']
    processed_text = text.lower()
    return jsonify(df2[df2.Player == processed_text].to_dict(orient='records'))


if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)