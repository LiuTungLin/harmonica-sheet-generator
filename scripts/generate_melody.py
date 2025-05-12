import os
import warnings
from note_seq.protobuf import generator_pb2
from note_seq.protobuf.music_pb2 import NoteSequence
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from style_config import style_definitions

# 關閉 TensorFlow INFO/WARNING
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 載入模型 bundle（相對路徑）
BUNDLE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'models', 'lookback_rnn.mag')
_bundle = sequence_generator_bundle.read_bundle_file(BUNDLE_PATH)
_generator = melody_rnn_sequence_generator.get_generator_map()['lookback_rnn'](
    checkpoint=None, bundle=_bundle)
_generator.initialize()

def generate_melody(style_name, tempo=120):
    """
    分段生成主旋律，依 style_config.py 的 structure 依序產生每段，再合併。

    參數:
      style_name: str, 音樂風格
      tempo: int, BPM
    回傳:
      NoteSequence（整段旋律）
    """
    if style_name not in style_definitions:
        raise ValueError(f"未定義風格: {style_name}")

    style = style_definitions[style_name]
    seconds_per_beat = 60.0 / tempo
    seconds_per_bar = seconds_per_beat * 4  # 固定 4 拍一小節

    merged = NoteSequence()
    merged.tempos.add(qpm=tempo)
    current_time = 0.0

    # 逐 section 分段生成
    for section_name, bars in style["structure"]:
        base_chords = style["chords"].get(section_name, [])
        if not base_chords:
            continue
        # 根據 bars 數量，以循環方式填滿每小節的和弦
        section_chords = [base_chords[i % len(base_chords)] for i in range(bars)]
        num_bars = len(section_chords)
        total_seconds = num_bars * seconds_per_bar

        # Primer：只有 tempo
        primer = NoteSequence()
        primer.tempos.add(qpm=tempo)

        # 設定生成範圍與和弦參數
        gen_options = generator_pb2.GeneratorOptions()
        sec = gen_options.generate_sections.add()
        sec.start_time = 0
        sec.end_time = total_seconds
        gen_options.args['chords'].string_value = ','.join(section_chords)

        # 呼叫模型生成這段旋律
        part = _generator.generate(primer, gen_options)

        # 平移並合併
        for note in part.notes:
            new_note = merged.notes.add()
            new_note.pitch = note.pitch
            new_note.start_time = note.start_time + current_time
            new_note.end_time = note.end_time + current_time
            new_note.velocity = note.velocity
            new_note.instrument = note.instrument

        current_time += total_seconds
        merged.total_time = current_time

    return merged
