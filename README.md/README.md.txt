from flask import Flask,render_template,request,redirect,flash,make_response
import os
app=Flask(__name__)
flight_numbers=["1234","5678","9876","6543"]
flight_times=["12:30","01:00","03:45","15:00"]
username_list=["ali","aram","ahlam","artam"]
password_list=["12al","ram2","ahl45","art98"]
app.config['SECRET_KEY']='EGRGTHTH'
path="./static/img/"

@app.route('/panel')
def panel():
    if request.cookies.get("user"):
         return render_template("panel.html",user=request.cookies.get("user"),profile=path)

    else:
        flash("plese first login","info")
        return redirect("/login")

@app.route("/login",methods=['GET', 'POST'])
def login():
   if request.method=='POST':
      Found=False
      for i in range(len(username_list)):
         if request.form.get("username")==username_list[i] and request.form.get("password") == password_list[i]:
            Found=True
            flash("login successfully", "success")
            response=make_response(redirect('/panel'))
            response.set_cookie("user",request.form.get('username'))
            return response

      if Found==False:
         return redirect("/login")
         flash("username or password invalid", "danger")
   else:
      return render_template("login.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
   if request.method=='POST':
      Found=False
      for i in range(len(username_list)):
          if request.form.get("username")==username_list[i] and request.form.get("password")==password_list:
              Found=True
              return redirect('/register')


      if Found==False:
          if request.form.get("password")==request.form.get("re_password"):
              username_list.append(request.form.get("username"))
              password_list.append(request.form.get("password"))
              flash("registered successfully", "success")
              return redirect("/login")
          else:
              return redirect("/register")
   else:
      return render_template("register.html")

@app.route('/',methods=['GET','POST'])
def flights():
    return render_template("index_2.html",items=len(flight_numbers),flight_numbers=flight_numbers,flight_times=flight_times,user=request.cookies.get('user'))

@app.route('/about')
def about():
    return render_template("about_2.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        alfa=request.form.get("f_num")
        beta = request.form.get("f_time")
        flight_numbers.append(alfa)
        flight_times.append(beta)
        flash("flight number added", "info")
        return redirect('/')

    else:
        return render_template("add_2.html")

@app.route('/delete',methods=['GET', 'POST'])
def delete():
    if request.method=='POST':
        for i in range(len(flight_numbers)):
            if flight_numbers[i]==request.form.get("flight_num"):
               flight_numbers.remove(flight_numbers[i])
               flight_times.remove(flight_times[i])
               break
        flash("flight number deleted", "danger")
        return redirect('/')

    else:
        return render_template("delete_2.html")

@app.errorhandler(404)
def eror(eror):
    return render_template("404.html"),404

@app.route("/logout")
def logout():
    response=make_response(redirect('/login'))
    response.delete_cookie('user')
    return response

@app.route('/profile',methods=["POST","GET"])
def profile():
    if request.cookies.get("user"):
        if request.method=="POST":
            response=make_response(redirect("/panel"))
            if request.form.get("new_username"):
                for i in range(len(username_list)):
                    if username_list[i]==request.cookies.get("user"):
                        username_list[i]=request.form.get("new_username")
                        flash("username changed successfully","success")
                        response.delete_cookie("user")
                        response.set_cookie("user",request.form.get("new_username"))
                        profile_name=request.form.get("new_username")
            else:
                profile_name=request.cookies.get("user")
            if request.files.get("profile"):
                profile=request.files.get("profile")
                profile.save(os.path.join(path,profile_name+".jpg"))
            return response
        else:
            return render_template("profile.html", user=request.cookies.get("user"))
    else:
        return redirect("/login")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=1111,debug=True)