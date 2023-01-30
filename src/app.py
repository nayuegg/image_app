from flask import Flask, render_template, request, redirect
import io
from PIL import Image
import base64

app = Flask(__name__)

##アップロードされる拡張子の制限
ALLOWED_EXTENTIONS = set(["png", "jpg", "gif", "jpeg"])

#拡張子が適切かを確認する関数
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS

#URLにアクセスがあった時の挙動の設定
@app.route("/", methods=["GET", "POST"])
def predicts():
    if request.method == "POST":
        #ファイルがなかった場合の処理
        if "filename" not in request.files:
            return redirect(request.url)
        
        #ファイルがあった場合のデータの取り出しの設定
        file = request.files["filename"]
        #ファイルの拡張子チェック
        if file and allowed_file(file.filename):
            #画像ファイルに対する処理
            #画像書き込み用のバッファを用意.画像を一時的に蓄える記憶装置
            buf = io.BytesIO()
            image = Image.open(file)
            #imageをバッファに書き込む
            image.save(buf, "png")
            #バッファに入れた画像のバイナリコードをbase64でエンコードしてutf-8でデコード
            base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
            #デコードしたものをHTML側のソースの記述に合わせるために付帯情報を付与する
            base64_data = "data:image/png;base64,{}".format(base64_str)
            #画像がアップロードされたときに表示するメッセージを設定
            message_ = "画像がアップロードされました。"
            return render_template("result.html", message=message_, image=base64_data)
        return redirect(request.url)

    elif request.method == "GET":
        return render_template("index.html")

#アプリケーションの実行を定義
if __name__ == "__main__":
    app.run(debug=True)