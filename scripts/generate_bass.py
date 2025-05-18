from note_seq.protobuf.music_pb2 import NoteSequence
from chords import all_chords
from style_config import style_definitions
from generate_chords import get_chord_progression

ELECTRIC_BASS = 33
REST_PREFIX = "#"

def generate_bass(style_name, tempo=120, instrument=ELECTRIC_BASS, velocity=80):
    """
    根據風格名稱與節奏，生成低音線。

    參數:
      style_name: str，音樂風格名稱
      tempo: int，BPM
      instrument: int，MIDI 樂器編號
      velocity: int，演奏強度

    回傳:
      NoteSequence (低音軌)
    """
    # 取得和弦進行與對應節奏列表
    chords_list, rhythms_per_chord = get_chord_progression(style_name)

    # 建立 NoteSequence
    seq = NoteSequence()
    seq.tempos.add(qpm=tempo)

    seconds_per_beat = 60.0 / tempo
    current_time = 0.0

    # 依對應節奏，為每個和弦播放低音根音
    for chord, pattern in zip(chords_list, rhythms_per_chord):
        # 取該和弦最低音為 bass root，並下移一個八度
        pitches = all_chords.get(chord, all_chords.get('C', []))
        root_pitch = pitches[0] - 12 if pitches else 36  # default to C2 if empty
        for dur in pattern:
            # 處理休止符
            if isinstance(dur, str) and dur.startswith(REST_PREFIX):
                current_time += float(dur[1:]) * seconds_per_beat
                continue

            # 播放低音音符
            dur_seconds = dur * seconds_per_beat
            note = seq.notes.add()
            note.pitch = root_pitch
            note.start_time = current_time
            note.end_time = current_time + dur_seconds
            note.velocity = velocity
            note.instrument = instrument

            current_time += dur_seconds

    seq.total_time = current_time
    return seq