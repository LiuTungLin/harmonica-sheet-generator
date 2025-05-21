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

    # 根據段落結構，設定每小節模式：
    # Intro/Outro 固定模式1 (全部根音)
    # 其他段落交替模式2與模式3
    structure = style_definitions[style_name]["structure"]
    modes_per_chord = []
    flip = True  # 用於在段落間交替模式2與3
    for section_name, bars in structure:
        if section_name in ["Intro", "Outro"]:
            modes_per_chord.extend([1] * bars)
        else:
            mode = 2 if flip else 3
            modes_per_chord.extend([mode] * bars)
            flip = not flip

    # 建立 NoteSequence
    seq = NoteSequence()
    seq.tempos.add(qpm=tempo)
    seconds_per_beat = 60.0 / tempo
    current_time = 0.0

    # 每個小節依對應節奏與模式播放低音
    for chord, pattern, mode in zip(chords_list, rhythms_per_chord, modes_per_chord):
        # 取得和弦根、三度與五度
        pitches = all_chords.get(chord, all_chords.get('C', []))
        if len(pitches) >= 3:
            root, third, fifth = pitches[0]-12, pitches[1]-12, pitches[2]-12
        else:
            root, third, fifth = 48, 52, 55  # C chord fallback

        # 根據模式設定輪替音高
        if mode == 1:
            cycle_pitches = [root]
        elif mode == 2:
            cycle_pitches = [root, third, fifth]
        else:
            cycle_pitches = [root + 12, fifth, third]

        # 每小節內重置 step
        step = 0
        for dur in pattern:
            if isinstance(dur, str) and dur.startswith(REST_PREFIX):
                current_time += float(dur[1:]) * seconds_per_beat
            else:
                dur_seconds = dur * seconds_per_beat
                note = seq.notes.add()
                note.pitch = cycle_pitches[step % len(cycle_pitches)]
                note.start_time = current_time
                note.end_time = current_time + dur_seconds
                note.velocity = velocity
                note.instrument = instrument
                current_time += dur_seconds
                step += 1

    seq.total_time = current_time
    return seq
