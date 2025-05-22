import os
import datetime
import tkinter as tk
from tkinter import ttk
from note_seq import sequence_proto_to_midi_file
from note_seq.protobuf import music_pb2
from generate_melody import generate_melody
from generate_bass import generate_bass
from generate_chords import get_chord_progression, generate_chords

def merge_sequences(sequences):
    merged = music_pb2.NoteSequence()
    for seq in sequences:
        merged.notes.extend(seq.notes)
        merged.text_annotations.extend(seq.text_annotations)
        merged.total_time = max(merged.total_time, seq.total_time)
    merged.tempos.add(qpm=sequences[0].tempos[0].qpm)
    return merged

def generate_midi(style_name="Pop", tempo=120):
    chords_list, rhythm_pattern = get_chord_progression(style_name)
    melody_seq = generate_melody(style_name, tempo)
    bass_seq   = generate_bass(style_name, tempo)
    chords_seq = generate_chords(chords_list, rhythm_pattern, tempo)

    merged_seq = merge_sequences([melody_seq, bass_seq, chords_seq])
    merged_seq.tempos[0].qpm = tempo

    filename = f"harmonica_sheet_{datetime.datetime.now():%Y%m%d%H%M}_{style_name}.mid"
    output_path = os.path.join(os.path.dirname(__file__), '..', 'midis', filename)
    sequence_proto_to_midi_file(merged_seq, output_path)
    status_label.config(text=f"已生成：{filename}")

def on_generate():
    style = style_var.get()
    tempo = int(tempo_var.get())
    generate_midi(style_name=style, tempo=tempo)

# 建立 GUI 視窗
window = tk.Tk()
window.title("MIDI 產生器")
window.geometry("320x200")

# 音樂風格選單
style_var = tk.StringVar(value="Folk")
ttk.Label(window, text="選擇風格").pack(pady=5)
style_menu = ttk.Combobox(window, textvariable=style_var, values=[
    "Modern", "Ashanti", "Ewe", "Funk", "Ballad", 
    "Reggae", "Rock", "Disco", "Pop", "Blues", 
    "Jazz", "Hiphop", "Samba", "Tango", "Folk"
], state="readonly")
style_menu.pack()

# 節奏輸入
tempo_var = tk.StringVar(value="120")
ttk.Label(window, text="節奏 (BPM)").pack(pady=5)
tempo_entry = ttk.Entry(window, textvariable=tempo_var)
tempo_entry.pack()

# 生成按鈕
generate_btn = ttk.Button(window, text="生成 MIDI", command=on_generate)
generate_btn.pack(pady=10)

# 狀態文字
status_label = ttk.Label(window, text="")
status_label.pack()

# 啟動主視窗
window.mainloop()
