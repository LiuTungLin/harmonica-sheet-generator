from note_seq import midi_io
from pathlib import Path

# 取得專案根目錄
project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / 'midis'

def generate_melody(style_name='pop', tempo=120):
    # 找到 output_dir 中最新的 MIDI 檔案
    midi_files = list(output_dir.glob('*.mid'))
    if not midi_files:
        print("沒有找到 MIDI 檔案")
        return
    
    latest_midi = max(midi_files, key=lambda x: x.stat().st_mtime)
    print(f"處理的最新 MIDI 檔案: {latest_midi.name}")
    
    # 讀取 MIDI 檔案並轉換為 NoteSequence
    note_sequence = midi_io.midi_file_to_note_sequence(str(latest_midi))
    return note_sequence
