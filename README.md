# harmonica-sheet-generator
本專案提供一個口琴三重奏樂譜的生成工具，使用者可以輸入音樂風格與速度(BPM)，將輸出的 MIDI 檔案匯入製譜軟體或 DAW 進行後續調整。

## 介紹
本系統生成的 MIDI 檔案分為三軌，主旋律、和弦、低音。
- 主旋律：<br>
  - 使用 magenta 的 [improv_rnn](https://github.com/magenta/magenta/tree/main/magenta/models/improv_rnn)，該模型使用 LSTM 將語言建模應用於旋律生成，並將旋律基於底層和弦進行條件化。
  - 在生成的每一步，模型會將目前和弦作為輸入，並輸出適合該和弦的旋律。
- 和弦：<br>
  - 使用 [HOHNER CHORD 48 和弦口琴](https://harmonica.tw/product/hohner-chord-48/)的所有和弦及其組成音，以及預先定義好的曲式結構及和弦進行。
  - 其和弦組合如下：<br>
大調和弦：F#, Db, Ab, Eb, Bb, F, C, G, D, A, E, B<br>
屬七和弦：Db7, Ab7, Eb7, Bb7, F7, C7, G7,D7, A7, E7, B7, F#7<br>
小調和弦：F#m, Dbm, Abm, Ebm, Bbm, Fm, Cm, Gm, Dm, Am, Em, Bm<br>
增減和弦：Db_aug, Ab_dim7, Eb_aug, Bb_dim7, Bb_aug, C_dim7, G_aug, D_dim7, A_aug, E_dim7, E_aug, F#dim7<br>

- 低音：<br>
  - 根據和弦的組成音及節奏樣式生成。
  - 在開頭與結尾兩個段落皆使用和弦的根音。
  - 中間段落則採用和弦的上行琶音與下行琶音交錯使用。

### 風格、和弦進行、節奏樣式
- 本系統參考了 [All Era Music](https://alleramusic.com/) 中的 [Music Rhythms](https://alleramusic.com/rhythms) 與 [Chords Progressions](https://alleramusic.com/progressions)。
- 各風格的和弦進行與節奏樣式定義在 style_config.py 中。


## 安裝
1. 請先確保已安裝 Anaconda / Miniconda 並設定好環境變數
2. 將專案複製到本機
    ```
    git clone https://github.com/LiuTungLin/harmonica-sheet-generator.git
    ```
3. 使用 conda 安裝 Python 環境
    ```
    conda create -n music python=3.8
    ```
4. 啟動環境
    ```
    conda activate music
    ```
5. 安裝套件
    ```
    pip install -r requirements.txt
    ```

## 快速開始
1. 進入 scripts 資料夾
    ```
    cd scripts
    ```
2. 執行腳本  

    2.1 使用預設參數(style: Folk, tempo: 120)
    ```
    python generate_midi.py
    ```
    2.2 手動調整參數  

    可選擇風格：Modern, Ashanti, Ewe, Funk, Ballad, Reggae, Rock, Disco, Pop, Blues, Jazz, Hiphop, Samba, Tango, Folk
    ```
    python generate_midi.py --style Folk --tempo 120
    ```
    2.3 使用圖形化介面  

    可從GUI選擇現有風格
    ```
    python ui.py
    ```
    2.4 使用網頁  

    ```
    python app.py
    ```
    開啟瀏覽器輸入網址
    ```
    http://localhost:5000/
    ```
3. 輸出的 MIDI 檔案會保存於 midis 資料夾中