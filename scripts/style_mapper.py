from sentence_transformers import SentenceTransformer, util

style_description = {
    "Modern": "Modern, 現代, 創新語言, 無調性實驗, 十二音序列, 印象主義色彩, 表現主義張力, 新古典結構, 電子音色探索, 非對稱節奏, 前衛氛圍, 都市機械感",
    "Ashanti": "Ashanti, 阿山蒂, 現代 R&B 味道, 嘻哈靈魂線條, 柔和女聲, 朗朗旋律, 合唱呼應, 女性賦權, 都市節奏風, 懷舊合成器, 情歌女王風格",
    "Ewe": "Ewe, 伊維, 西非多層鼓樂, 3:2 交叉節奏, Call-and-Response, batucada 打擊, Gankogui 節奏鐘, Axatse 葫蘆鈴, 社會祭典音樂, 戰舞氣勢",
    "Funk": "Funk, 放克, 打破切分十六分, 貝斯 Groove, 銅管爆發, James Brown 式強音, 電子合成 Bassline, 即興 Solo, 社會意識歌詞",
    "Ballad": "Ballad, 情歌, 抒情敘事, 慢板鋼琴間奏, 情感轉折, 簡潔旋律, 民謠底蘊, 結他伴奏氛圍, 唱腔張力",
    "Reggae": "Reggae, 雷鬼, 牙買加 One-Drop, offbeat 吉他 skank, 深沉貝斯線, 回聲延遲 Dub, Rastafari 詩意, 社會政治歌詞",
    "Rock": "Rock, 搖滾, 電吉他破音, 重拍強調, 吉他 Solo, 現場即興, 青春反叛, 強力鼓點, 現場舞台能量",
    "Disco": "Disco, 迪斯可, 四拍重音, 同步鼓機, 弦管鋪陳, Studio 54 派對, 鋁箔舞池氛圍, LGBTQ+ 慶典精神",
    "Pop": "Pop, 流行, 朗朗旋律, 副歌重複, 特色編曲, 廣播友善, 電子製作感, 商業元素, 即時共鳴",
    "Blues": "Blues, 藍調, 非裔美國根源, 12 小節進行, AAB 結構, 藍音符滑音, 滑音吉他, 口琴哀愁, 即興呼應",
    "Jazz": "Jazz, 爵士, 即興即刻創造, 搖擺律動, 複雜擴展和弦, 切分律動, 大編制銅管, 自由爵士探索",
    "Hiphop": "Hiphop, 嘻哈, 節奏機取樣, 808 鼓機, 刮盤 DJing, MC 饒舌節奏, 街頭塗鴉文化, 社會批判詞",
    "Samba": "Samba, 森巴, 巴西嘉年華, batucada 節奏群, pandeiro 拍手鼓, cuíca 呼號, call-and-response, 舞蹈慶典感",
    "Tango": "Tango, 探戈, bandoneón 憂鬱, 切分節奏, 小提琴對唱, 舞伴情感, Piazzolla 新探戈, 黃金時期復古",
    "Folk": "Folk, 民謠, 口耳相傳, 原聲吉他伴奏, 敘事歌詞, 區域傳統旋律, 班卓琴指彈, 民間傳唱, 賦權議題"
}

# 載入預訓練模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 將 style 描述轉成句向量
style_keys = list(style_description.keys())
style_texts = [style_description[k] for k in style_keys]
style_embeddings = model.encode(style_texts, convert_to_tensor=True)

def map_style(user_input: str):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    # 計算餘弦相似度
    cos_scores = util.cos_sim(input_embedding, style_embeddings)[0]
    best_idx = cos_scores.argmax().item()
    return style_keys[best_idx], cos_scores[best_idx].item()

if __name__ == "__main__":
    user_text = "爵士藍調"
    style, score = map_style(user_text)
    print(f"最相似風格: {style} (相似度: {score:.3f})")
