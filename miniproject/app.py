from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://Han:wjdrb1322@cluster0.ckbkppy.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('han.html')

@app.route("/api/reviews/show/", methods=["GET"])
def reviews_get():
    review_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': review_list})

@app.route('/api/reviews/save/', methods=['POST'] )
def reviews_save():

    comment_receive = request.form['comment_give']
    nickname_receive = request.form['nickname_give']

    review_list = list(db.reviews.find({}, {'_id': False}))
    count = len(review_list) + 1

    doc = {
        'num' : count,
        'comment' : comment_receive,
        'nickname' : nickname_receive
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

@app.route("/api/reviews/edit/<num>", methods=["POST"])
def reviews_edit(num):
    print(num)
    edit_nickname_receive = request.form['edit_nickname_give']
    edit_comment_receive = request.form['edit_comment_give']
    print(edit_comment_receive, edit_nickname_receive)
    db.reviews.update_one({'num':int(num)}, {'$set': {'nickname': edit_nickname_receive, 'comment': edit_comment_receive}})
    print(edit_comment_receive)
    return jsonify({'msg': '수정 완료!'})

@app.route("/api/reviews/load/<num>", methods=["GET"])
def reviews_load(num):
    print(num)
    review_list = list(db.reviews.find({'num':int(num)}, {'_id': False}))
    print(review_list)
    return jsonify({'reviews': review_list})

@app.route('/api/reviews/delete/<num>', methods=['GET'])
def reviews_delete(num):
    db.reviews.delete_one({'num': int(num)})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)