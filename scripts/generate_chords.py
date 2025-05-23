import random
from note_seq.protobuf.music_pb2 import NoteSequence
from chords import all_chords
from style_config import style_definitions

ACOUSTIC_GUITAR = 24
REST_PREFIX = "#"

def get_chord_progression(style_name):
    """
    根據風格名稱取得和弦進行與節奏。

    參數:
      style_name: str，例如 'Pop'
    回傳:
      chords_list: List[str]
      rhythm_pattern: List[float or str]
    """
    # 讀取風格設定
    if style_name not in style_definitions:
        raise ValueError(f"未定義風格: {style_name}")
    style = style_definitions[style_name]

    # 組合和弦進行
    chords_list = []
    for section_name, bars in style["structure"]:
        chord_seq = style["chords"].get(section_name, [])
        for i in range(bars):
            # 每小節使用 chord_seq 的第 i % len(chord_seq) 個和弦
            chords_list.append(chord_seq[i % len(chord_seq)])

    # 選擇節奏樣板
    rhythms_dict = style.get("rhythms", {})
    if rhythms_dict:
        # 隨機選一個節奏樣板值列表
        rhythm_pattern = random.choice(list(rhythms_dict.values()))
    else:
        rhythm_pattern = [1, 1, 1, 1]

    return chords_list, rhythm_pattern


def generate_chords(chords_list, rhythm_pattern, tempo=120, instrument=ACOUSTIC_GUITAR, velocity=50):
    """
    根據和弦清單與節奏生成 NoteSequence。

    chords_list: List[str]，例如 ["C", "G", "Am", ...]
    rhythm_pattern: List[float or str]，拍數列表，字串開頭 '#' 表示休止
    tempo: int，BPM
    instrument: int，MIDI 樂器編號
    velocity: int，演奏強度
    """
    seq = NoteSequence()
    seq.tempos.add(qpm=tempo)
    seconds_per_beat = 60.0 / tempo
    current_time = 0.0

    for chord in chords_list:
        pitches = all_chords.get(chord)

        if pitches is None:
            print(f"警告: 和弦 {chord} 未定義，將使用 C 和弦代替。")
            pitches = all_chords["C"]
            
        for dur in rhythm_pattern:
            # 休止符
            if isinstance(dur, str) and dur.startswith(REST_PREFIX):
                current_time += float(dur[1:]) * seconds_per_beat
                continue

            # 演奏和弦
            dur_seconds = dur * seconds_per_beat
            for pitch in pitches:
                note = seq.notes.add()
                note.pitch = pitch
                note.start_time = current_time
                note.end_time = current_time + dur_seconds
                note.velocity = velocity
                note.instrument = instrument

            current_time += dur_seconds

    seq.total_time = current_time
    return seq