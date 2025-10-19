from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    ten = request.form.get('ten')
    tuoi = request.form.get('tuoi')
    que = request.form.get('que')
    congviec = request.form.get('congviec')
    diem = request.form.get('diem')
    return render_template('thongtin.html',
                           ten=ten,
                           tuoi=tuoi,
                           que=que,
                           congviec=congviec,
                           diem=diem)        

if __name__ == '__main__':
    app.run(debug=True)