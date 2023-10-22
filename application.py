from flask import Flask, render_template, request, redirect, jsonify
# import sys
import hashlib
import time
from datetime import datetime

app = Flask(__name__)
count = 1
block = None
blockchain_data = []


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user1")
def hello():
    return render_template("user1.html", blockchain_data=blockchain_data)

@app.route("/user2")
def user2():
    return render_template("user2.html", blockchain_data=blockchain_data)

@app.route("/user3")
def user3():
    return render_template("user3.html", blockchain_data=blockchain_data)




@app.route('/submit', methods=['POST'])
def submit():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']
    # 데이터 처리 로직
    # print("보내는 사람:", sender)
    # print("받는 사람:", receiver)
    # print("금액:", amount)

    def valid_proof(nonce, transaction, previous_block):
        global guess_hash
        guess = f"{transaction}{previous_block}{nonce}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def blockchain():
        global count, block
        if count >= 2:
            previous_block = block
        else:
            previous_block = None
        transaction = {
            'index': count,
            'sender': sender,
            'recipient': receiver,
            'amount': amount,
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'previous_hash': previous_block
        }
        print(transaction)
        count = count + 1
        nonce = 0
        while not valid_proof(nonce, transaction, previous_block):
            nonce += 1


        block = guess_hash
        current_block={
            'number':count -1,
            'block':block,
            'nonce':nonce
        }
        blockchain_data.append(current_block)
        print(f"블록 해시: {block}")
        print(f"증명: {nonce}")

    blockchain()
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
