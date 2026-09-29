"""百人一首・下の句検索アプリ
   API連携でJSONデータを取得。ユーザー入力に対応した検索結果を表示する。
   表示ウィンドウにはtkinterを使用。
"""


import json
import requests
import tkinter as tk


# 連携先URL
url1 = "https://api.aoikujira.com/hyakunin/get2.php?fmt=json"

# APIデータをJSONで取得
res1 = requests.get(url1)

# JSONデータをpythonのリスト(辞書型の集まり)に変換する。
kekka1 = json.loads(res1.text)


def waka_search():
    """ユーザーが入力した上の句から百人一首を検索（前方一致）"""
    inputk = entry1.get().replace(" ", "").strip()

    # 前方一致する句の辞書をリストに追加（リスト内包表記）
    results = [val for val in kekka1 
               if str(val.get("kami_kana", "")).replace(" ", "").startswith(inputk)]

    # 表示用テキストボックスの初期化
    textbox1.delete(0.0, tk.END)
    textbox1.config(bg="white")

    # label2を画面内に配置する
    label2.place(x=430,y=35)

    if results:
        lines = []
        for val in results:
            no_str = str(val["no"]).zfill(2)
            item_text = (
                f"No_{no_str} {val['kami']}   {val['simo']}\n"
                f"   {val['kami_kana']}   {val['simo_kana']}\n"
                f"  {val['sakusya']}({val['sakusya_kana']})"
            )
            lines.append(item_text)

        # 各結果を区切り線で結合して一括挿入
        separator = f"\n{'-' * 80}\n"
        textbox1.insert(tk.END, separator.join(lines))
        label2.config(text=f"一致件数 {len(results)} 件")
    else:
        label2.config(text="一致する句がありません")


def textclear():
    """一括クリア"""
    entry1.delete(0, tk.END)
    textbox1.delete(0.0, tk.END)
    textbox1.config(bg="lightgray")
    label2.config(text="")
    label2.place_forget()  # 非表示として設定


# インスタンスの生成と基本情報の設定
root = tk.Tk()
root.title("百人一首検索アプリ")
root.minsize(650, 500)

# 背景の設定
photoimage = tk.PhotoImage(file="bgimg.png")
canvas = tk.Canvas(root, bg="white", width=660, height=510)
canvas.place(x=-2, y=-2)
canvas.create_image(0, 0, image=photoimage, anchor=tk.NW)

# ウィジェットの生成
label1 = tk.Label(text="前方一致で百人一首を検索できます", font=("メイリオ", 16, "bold"), fg="purple")
label2 = tk.Label(text="", font=("メイリオ", 12, "bold"), fg="purple")  # 最初から生成しておく
btn1 = tk.Button(text="検索", command=waka_search, padx=5)
btn2 = tk.Button(text="クリア", command=textclear, padx=5)
entry1 = tk.Entry(text="", width=60)
textbox1 = tk.Text(width=80, height=26, bg="lightgray")

# ウィジェットの配置
label1.place(x=50, y=30)
label2.place_forget()  # 非表示として設定
btn1.place(x=480, y=90)
btn2.place(x=550, y=90)
entry1.place(x=50, y=90)
textbox1.place(x=35, y=130)

# 画面表示の保持
root.mainloop()
