import os
import warnings
import datetime
from note_seq import sequence_proto_to_midi_file
from note_seq.protobuf import music_pb2
from generate_melody import generate_melody
from generate_bass import generate_bass
from generate_chords import get_chord_progression, generate_chords
from style_config import style_definitions

# 關閉 TensorFlow INFO/WARNING
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def merge_sequences(sequences):
    merged = music_pb2.NoteSequence()
    for seq in sequences:
        merged.notes.extend(seq.notes)
        merged.text_annotations.extend(seq.text_annotations)
        merged.total_time = max(merged.total_time, seq.total_time)
    # 共用第一軌的 tempo
    merged.tempos.add(qpm=sequences[0].tempos[0].qpm)
    return merged


def generate_midi(style_name="Pop", tempo=120):
    # 1. 取得和弦進行 + 節奏
    chords_list, rhythm_pattern = get_chord_progression(style_name)

    # 2. 呼叫三個模組
    melody_seq = generate_melody(style_name, tempo)
    bass_seq   = generate_bass(style_name, tempo)
    chords_seq = generate_chords(chords_list, rhythm_pattern, tempo)

    # 3. 合併
    merged_seq = merge_sequences([melody_seq, bass_seq, chords_seq])
    merged_seq.tempos[0].qpm = tempo

    # 4. 存檔
    filename = f"harmonica_sheet_{datetime.datetime.now():%Y%m%d%H%M}.mid"
    output_path = os.path.join(os.path.dirname(__file__), '..', 'midis', filename)
    sequence_proto_to_midi_file(merged_seq, output_path)
    print(f"已生成 MIDI: {output_path}")


if __name__ == "__main__":
    generate_midi(style_name="Pop", tempo=120)
