# harmonica-sheet-generator
本專案提供一個口琴三重奏樂譜的生成工具，使用者可以將輸出的 MIDI 檔案匯入製譜軟體或 DAW 進行後續調整。

## 介紹
本系統生成的 MIDI 檔案分為三軌，主旋律、和弦、低音。
- 主旋律：使用 magenta 的 melody_rnn，根據和弦序列來生成相應的旋律。
- 和弦： 使用 HOHNER CHORD 48 和弦口琴的所有和弦及其組成音，以及預先定義好的曲式結構及和弦進行。
- 低音：根據和弦的根音及節奏樣式生成。

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
2. 執行 generate_midi.py
    ```
    python generate_midi.py
    ```
3. 輸出的 MIDI 檔案會保存於 midis 資料夾中

## 調整
- 所有和弦及組成音皆定義於 chords.py 中，可以自行調整。
- 六大風格 ( Pop, Rock, Ballad, Folk, EDM, Lo-Fi ) 的曲式結構及個段落的和弦進行皆定義於 style_config.py，可以自行調整。