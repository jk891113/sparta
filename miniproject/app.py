from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://Han:wjdrb1322@cluster0.ckbkppy.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

# 홈
@app.route('/')
def index():
    return render_template('index.html')
# 한정규
@app.route('/han')
def han():
    return render_template('han.html')
# 박정훈
@app.route('/park')
def park():
    return render_template('park.html')
# 이신희
@app.route('/lee')
def lee():
    return render_template('lee.html')
# 최찬호
@app.route('/choi')
def choi():
    return render_template('choi.html')



# index.html

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





# han.html

@app.route("/api/reviews/show", methods=["GET"])
def reviews_get():
    review_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': review_list})

@app.route('/api/reviews/save', methods=['POST'] )
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





# park.html

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




# choi.html

@app.route("/api/notes", methods=["GET"])
def get():
    data = list(db.ex.find({}, {"_id": False}))

    return jsonify({"data": data})


@app.route("/api/notes", methods=["POST"])
def post():
    name = request.form["name"]
    text = request.form["text"]
    identifier = get_identifier()

    doc = {
        "id": identifier,
        "name": name,
        "text": text
    }

    db.ex.insert_one(doc)
    return jsonify({"msg": "등록 완료"})


@app.route("/api/notes/<target>", methods=["POST"])
def edit(target):
    print(target)
    name = request.form["name"]
    text = request.form["text"]

    db.ex.update_one({"id": int(target)}, {"$set": {"text": text, "name": name}})

    return jsonify({"msg": "업데이트 완료"})


@app.route("/api/notes/<target>", methods=["GET"])
def put(target):
    print(target)
    data = list(db.ex.find({}, {"_id": False}))

    return jsonify({"data": data})


@app.route("/api/notes/<target>", methods=["DELETE"])
def delete(target):
    print(target)

    db.ex.delete_one({"id": int(target)})

    return jsonify({"msg": "삭제완료"})


def get_identifier():
    return len(list(db.ex.find({}, {"_id": False})))




# lee.html

@app.route("/notes", methods=["POST"])
def notes_post():
    writer_receive = request.form['writer_give']
    content_receive = request.form['content_give']

    doc = {
        'writer': writer_receive,
        'content': content_receive
    }

    db.notes.insert_one(doc)
    return jsonify({'msg':'작성 완료'})

@app.route("/notes", methods=["GET"])
def notes_get():
    comment_list = list(db.notes.find({},{'_id':False}))
    return jsonify({'comment':comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)