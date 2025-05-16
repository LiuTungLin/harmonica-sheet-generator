import subprocess
from note_seq import midi_io
from pathlib import Path
from generate_chords import get_chord_progression

# 專案根目錄
project_root = Path(__file__).resolve().parent.parent

# 相對路徑
bundle_file = project_root / 'models' / 'chord_pitches_improv.mag'
output_dir = project_root / 'midis'

# 將 Path 物件轉換為字串
bundle_file_str = str(bundle_file)
output_dir_str = str(output_dir)

def generate_improv_midi(style_name='Folk'):
    # 取得對應風格的和弦進行
    chords_list, rhythm_pattern = get_chord_progression(style_name)
    chords_string = ' '.join(chords_list)

    # 定義各個參數
    config = 'chord_pitches_improv'
    num_outputs = '1'
    primer_melody = '[55]'
    backing_chords = chords_string
    steps_per_chord = '16'

    # 建立命令列參數列表
    cmd = [
        'improv_rnn_generate',
        f'--config={config}',
        f'--bundle_file={bundle_file_str}',
        f'--output_dir={output_dir_str}',
        f'--num_outputs={num_outputs}',
        f'--primer_melody={primer_melody}',
        f'--backing_chords={backing_chords}',
        f'--steps_per_chord={steps_per_chord}'
    ]

    try:
        # 執行命令
        subprocess.run(cmd, check=True)
        print("主旋律 MIDI 檔案生成完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"執行 improv_rnn_generate 時發生錯誤: {e}")
        return False

def generate_melody(style_name, tempo=120):
    # 先確保主旋律生成
    if generate_improv_midi(style_name):
        # 找到 output_dir 中最新的 MIDI 檔案
        midi_files = list(output_dir.glob('*.mid'))
        if not midi_files:
            print("沒有找到 MIDI 檔案")
            return
        
        latest_midi = max(midi_files, key=lambda x: x.stat().st_mtime)
        print(f"處理的最新 MIDI 檔案: {latest_midi.name}")

        # 讀取 MIDI 檔案並轉換為 NoteSequence
        note_sequence = midi_io.midi_file_to_note_sequence(str(latest_midi))

        # 刪除主旋律檔
        try:
            latest_midi.unlink()
            print(f"已刪除主旋律 MIDI 檔案：{latest_midi.name}")
        except Exception as e:
            print(f"刪除主旋律 MIDI 檔案失敗：{e}")
            
        return note_sequence
    
    else:
        print("轉換 note_sequence 失敗")
