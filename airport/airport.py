from flask import Flask,render_template,request,redirect
app=Flask(__name__)
flight_number=["1111","2222","3333"]
flight_time=["12:20","13:00","02:30"]
@app.route('/')
def home():
     return render_template("index.html",f_number=flight_number,f_time=flight_time,items=len(flight_number))

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/add handler',methods=['GET','POST'])
def add_handler():
    if len(request.form.get('f_number'))==4:
       flight_number.append(request.form.get('f_number'))
       flight_time.append(request.form.get('f_time'))
       return redirect('/')
    else:
        return redirect('/add')

@app.route('/delete')
def delete():
    return render_template("delete.html")

@app.route('/delete handler',methods=['GET','POST'])
def delete_handler():
    for i in range(len(flight_number)):
        if flight_number[i]==request.form.get('f_number'):
            flight_number.remove(flight_number[i])
            flight_time.remove(flight_time[i])
            break
    return redirect('/')
@app.errorhandler(404)
def eror(eror):
    return render_template("404.html"),404


if __name__=='__main__':
    app.run(host='0.0.0.0',port=1111,debug=True)


