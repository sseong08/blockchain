from flask import Flask, render_template, request, redirect
import hashlib
import time
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  #사용자 1,2,3을 선택할 수 있는 페이지

@app.route("/user1")
def hello():
    return render_template("user1.html", blockchain_data=blockchain_data) #사용자 1로 연결

@app.route("/user2")
def user2():
    return render_template("user2.html", blockchain_data=blockchain_data) #사용자 2로 연결

@app.route("/user3")
def user3():
    return render_template("user3.html", blockchain_data=blockchain_data) #사용자 3으로 연결



count = 1
block = None
blockchain_data = []


@app.route('/submit', methods=['POST']) #GET과 POST형식 중 POST형식으로 데이터를 전달받음
def submit():
    sender = request.form['sender']      # 보내는 사람 값 받아오기
    receiver = request.form['receiver']  # 받는 사람 값 받아오기
    amount = request.form['amount']      # 금액의 값 받아오기

    def valid_proof(nonce, transaction, previous_block):         
        global guess_hash
        guess = f"{transaction}{previous_block}{nonce}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def blockchain():
        global count, block         #count와 block을 전역변수로 선언
        if count >= 2:              #만약 count가 2보다 크다면 블록의 값을 이전 블록으로 전환하기
            previous_block = block
        else:                       #count가 1이면 이전블록의 값은 none
            previous_block = None
        transaction = {             #거래내역에는 블록의 번호, 보내는사람, 받는사람, 금액, 거래가 이루어진 시간, 이전블록의 값이 들어감
            'index': count,
            'sender': sender,
            'recipient': receiver,
            'amount': amount,
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'previous_hash': previous_block
        }
        print(transaction)
        
        count = count + 1         #count를 1올린다
        nonce = 0                 #nonce를 0으로 설정(초기값)
        while not valid_proof(nonce, transaction, previous_block): #vaild_proof의 함수가 참이 될때까지 반복
            nonce += 1 #nonce의 값을 1씩 증가시키며 증명확인 계산


        block = guess_hash        # 블록을 4개의 0으로 시작하는 guess_hash로 정의
        current_block={           # 현재 블록의 number, 해시값, nonce를 저장
            'number':count -1,
            'block':block,
            'nonce':nonce
        }
        blockchain_data.append(current_block)
        print(f"블록 해시: {block}")
        print(f"증명: {nonce}")

    blockchain()
    return redirect(request.referrer) #이전 페이지로 돌아가는 코드

if __name__ == "__main__":
    app.run(host='0.0.0.0')
