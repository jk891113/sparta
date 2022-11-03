from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:sparta@cluster0.xcyvm7t.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/mypagepark", methods=["GET"])
def mypage():
   return render_template("park.html")


@app.route("/notes", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.mypage.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'count':  count,
           'name': name_receive,
           'comment': comment_receive,
           }
    db.mypage.insert_one(doc)

    return jsonify({'msg':'방명록 추가 완료!!'})

@app.route("/notes", methods=["GET"])
def homework_get():
    comment_list = list(db.mypage.find({}, {'_id': False}))

    return jsonify({'comment': comment_list})

# 이때 GET으로 받은 count 값이 string으로 나오고 있으므로 int 형변형 하고, list값으로 받아야함. find_one은 찾는 것이고 list 값으로 받아지지 않음.
@app.route("/notes/update/<count>", methods=["GET"])
def homework_update(count):
    print(count)
    count_list = list(db.mypage.find({'count': int(count)}, {'_id': False}))
    # count_list = db.mypage.find_one({'count': int(count)}, {'_id': False})
    print(count_list)
    return jsonify({'comment': count_list})

# 넘겨 받은 name값과,comment값을 입력 후 -> DB 수정하는 코드로 수정. 몽고DB update코드는 불러온 count값으로 db를 찾고 $set을 사용하여 name,comment의 value를 수정함..
@app.route("/notes/update/<count>", methods=["POST"])
def homework_updatepost(count):
    print(count)
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    print(name_receive, comment_receive)
    db.mypage.update_one({'count': int(count)}, {'$set': {'name': name_receive,'comment':comment_receive}})

    return jsonify({'msg':'방명록 수정 완료!!'})


# 넘긴 카운트 값을 파이썬에서 받음 <> <<--받는 문법, 파라미터에 count를 넣어 <count> 안에있는 값을 받아옴. 받아온 count 값이 string 타입이라 int 타입으로 형변환을 해줘야함.
# 받아오는 값이 어떤건지 궁금 할때는 print로 찍어보면 get으로 무엇을 받아오는지 알 수 있음.
@app.route("/notes/delete/<count>", methods=["GET"])
def homework_delete(count):

    db.mypage.delete_one({'count': int(count)})

    return jsonify({'msg': '삭제 완료!'})





########### index페이지 백단 연결 ###############


@app.route("/index/notes", methods=["POST"])
def homework_post1():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.index.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'count':  count,
           'name': name_receive,
           'comment': comment_receive,
           }
    db.index.insert_one(doc)

    return jsonify({'msg':'방명록 추가 완료!!'})

@app.route("/index/notes", methods=["GET"])
def homework_get1():
    comment_list = list(db.index.find({}, {'_id': False}))

    return jsonify({'comment': comment_list})

# 이때 GET으로 받은 count 값이 string으로 나오고 있으므로 int 형변형 하고, list값으로 받아야함. find_one은 찾는 것이고 list 값으로 받아지지 않음.
@app.route("/index/notes/update/<count>", methods=["GET"])
def homework_update1(count):
    print(count)
    count_list = list(db.index.find({'count': int(count)}, {'_id': False}))
    # count_list = db.mypage.find_one({'count': int(count)}, {'_id': False})
    print(count_list)
    return jsonify({'comment': count_list})

# 넘겨 받은 name값과,comment값을 입력 후 -> DB 수정하는 코드로 수정. 몽고DB update코드는 불러온 count값으로 db를 찾고 $set을 사용하여 name,comment의 value를 수정함..
@app.route("/index/notes/update/<count>", methods=["POST"])
def homework_updatepost1(count):
    print(count)
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    print(name_receive, comment_receive)
    db.index.update_one({'count': int(count)}, {'$set': {'name': name_receive,'comment':comment_receive}})

    return jsonify({'msg':'방명록 수정 완료!!'})


# 넘긴 카운트 값을 파이썬에서 받음 <> <<--받는 문법, 파라미터에 count를 넣어 <count> 안에있는 값을 받아옴. 받아온 count 값이 string 타입이라 int 타입으로 형변환을 해줘야함.
# 받아오는 값이 어떤건지 궁금 할때는 print로 찍어보면 get으로 무엇을 받아오는지 알 수 있음.
@app.route("/index/notes/delete/<count>", methods=["GET"])
def homework_delete1(count):

    db.index.delete_one({'count': int(count)})

    return jsonify({'msg': '삭제 완료!'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)