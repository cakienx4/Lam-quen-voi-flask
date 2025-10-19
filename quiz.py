from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

DATA_FILE = "questions.json"

# --- Hàm tiện ích đọc & ghi file ---
def load_questions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_questions(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Nạp dữ liệu khi khởi động ---
questions = load_questions()

@app.route('/')
def main():
    return render_template('home.html')

# --- Thêm câu hỏi ---
@app.route('/tch', methods=['GET', 'POST'])
def them_cau_hoi():
    if request.method == 'POST':
        cauhoi = request.form['cauhoi']
        dapanA = request.form['dapanA']
        dapanB = request.form['dapanB']
        dapanC = request.form['dapanC']
        dapanD = request.form['dapanD']
        dapan_dung = request.form['dapandung']

        new_q = {
            'cauhoi': cauhoi,
            'dapan': [dapanA, dapanB, dapanC, dapanD],
            'dapan_dung': dapan_dung
        }

        questions.append(new_q)
        save_questions(questions)  # ⬅ Lưu lại ngay sau khi thêm
        return redirect(url_for('main'))
    
    return render_template('themcauhoi.html')

# --- Trả lời câu hỏi ---
@app.route('/tlch', methods=['GET', 'POST'])
def tra_loi_cau_hoi():
    if not questions:
        return "<h3>Chưa có câu hỏi nào! Hãy thêm trước đã.</h3><a href='/'>Quay lại</a>"

    if request.method == 'POST':
        tra_loi = {}
        for i, _ in enumerate(questions):
            tra_loi[i] = request.form.get(f'q{i}')
        return redirect(url_for('tinh_diem', answers=str(tra_loi)))

    return render_template('traloi.html', questions=questions)

# --- Tính điểm ---
@app.route('/diem')
def tinh_diem():
    import ast
    answers = ast.literal_eval(request.args.get('answers'))
    # ép key về int
    answers = {int(k): v for k, v in answers.items()}

    dung = 0
    for i, q in enumerate(questions):
        if answers.get(i) == q['dapan_dung']:
            dung += 1

    diem = round((dung / len(questions)) * 100, 2)
    return render_template('diem.html', questions=questions, answers=answers, diem=diem)

if __name__ == '__main__':
    app.run(debug=True)
