from flask import Flask,request,render_template,redirect,url_for

app=Flask(__name__)

@app.route("/")
def welcome():
    return "<b><h1>Welcome to this flsak Web app asdf</h1></b>"

@app.route("/home",methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/form',methods=['GET','POST'])
def form():
    return render_template('form.html')

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        return f'Hello {name}'
    return render_template('form.html')
#variable rule
# @app.route('/success/<int:score>')
# def success(score):
#     return f"Your marks is {score}"

@app.route('/success/<int:score>')
def success(score):
    res=""
    if score<50:
        res="Fail"
    else:
        res="Pass"
    exp={'score':score,"res":res}
    return render_template('result.html',results=exp)

@app.route('/successif/<int:score>')
def successif(score):
    return render_template('result.html',results=score)


@app.route('/getresult',methods=['GET','POST'])
def get_result():
    score_t=0
    if request.method=='POST':
        DS=request.form['DS']
        ML=request.form['ML']
        DV=request.form['DV']
        score_t=(int(DS)+int(ML)+int(DV))/3
    else:
       return render_template('marks.html')
    return redirect(url_for('successif',score=score_t))

if __name__=='__main__':
    app.run(debug=True)