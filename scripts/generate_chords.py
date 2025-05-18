import random
from note_seq.protobuf.music_pb2 import NoteSequence
from chords import all_chords
from style_config import style_definitions

ACOUSTIC_GUITAR = 24
REST_PREFIX = "#"

def get_chord_progression(style_name):
    """
    根據風格名稱取得和弦進行與各段落節奏。

    參數:
      style_name: str，例如 'Pop'
    回傳:
      chords_list: List[str]
      rhythms_per_chord: List[List[float or str]]
    """
    if style_name not in style_definitions:
        raise ValueError(f"未定義風格: {style_name}")
    style = style_definitions[style_name]

    # 取得每個段落可用的節奏模板群組
    rhythms_dict = style.get("rhythms", {})

    # 為每個段落隨機指派一個節奏樣板
    section_rhythms = {}
    for section_name, _ in style["structure"]:
        templates = rhythms_dict.get(section_name) or list(rhythms_dict.values())
        if not templates:
            section_rhythms[section_name] = [1, 1, 1, 1]
        else:
            section_rhythms[section_name] = random.choice(templates)

    # 組合和弦進行與對應節奏
    chords_list = []
    rhythms_per_chord = []
    for section_name, bars in style["structure"]:
        chord_seq = style["chords"].get(section_name, [])
        pattern = section_rhythms[section_name]
        for i in range(bars):
            chord = chord_seq[i % len(chord_seq)]
            chords_list.append(chord)
            rhythms_per_chord.append(pattern)

    return chords_list, rhythms_per_chord


def generate_chords(chords_list, rhythms_per_chord, tempo=120, instrument=ACOUSTIC_GUITAR, velocity=50):
    """
    根據和弦清單與節奏生成 NoteSequence。

    chords_list: List[str]
    rhythms_per_chord: List[List[float or str]]，每個和弦對應的節奏子列表
    tempo: int，BPM
    instrument: int，MIDI 樂器編號
    velocity: int，演奏強度
    """
    seq = NoteSequence()
    seq.tempos.add(qpm=tempo)
    seconds_per_beat = 60.0 / tempo
    current_time = 0.0

    for chord, pattern in zip(chords_list, rhythms_per_chord):
        pitches = all_chords.get(chord)
        if pitches is None:
            print(f"警告: 和弦 {chord} 未定義，將使用 C 和弦代替。")
            pitches = all_chords.get("C", [])

        for dur in pattern:
            # 處理休止符
            if isinstance(dur, str) and dur.startswith(REST_PREFIX):
                current_time += float(dur[1:]) * seconds_per_beat
            else:
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
