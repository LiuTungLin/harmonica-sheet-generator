import subprocess
from pathlib import Path

# 取得目前腳本所在的目錄
base_dir = Path(__file__).resolve().parent

# 建立相對於腳本的路徑
bundle_file = base_dir / 'models' / 'chord_pitches_improv.mag'
output_dir = base_dir / 'midis'

# 將 Path 物件轉換為字串，以供 subprocess 使用
bundle_file_str = str(bundle_file)
output_dir_str = str(output_dir)

def generate_improv_midi():
    # 定義各個參數
    config = 'chord_pitches_improv'
    num_outputs = '1'
    primer_melody = '[55]'
    backing_chords = 'G C D G G C D G G C D G C D G Em C D G Em G C D G G C D G C D G Em C D G Em G C D G'
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
    
def run_generate_midi():
    # 調用 generate_midi.py
    generate_midi_script = base_dir / 'scripts' / 'generate_midi.py'
    try:
        subprocess.run(['python', str(generate_midi_script)], check=True)
        print("generate_midi.py 執行完成")
    except subprocess.CalledProcessError as e:
        print(f"執行 generate_midi.py 時發生錯誤: {e}")

if __name__ == '__main__':
    # 呼叫 generate_improv_midi 並確保生成成功
    if generate_improv_midi():
        run_generate_midi()  # 如果生成成功，執行後續處理
