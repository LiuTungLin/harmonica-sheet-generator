import os
import warnings
import note_seq
from note_seq.protobuf import generator_pb2
from note_seq.protobuf.music_pb2 import NoteSequence
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle

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
    根據風格名稱與節奏，透過 Magenta Melody RNN 生成主旋律。

    參數:
      style_name: str, 音樂風格
      tempo: int, BPM
    回傳:
      NoteSequence
    """
    # 1. 從 generate_chords 模組取得和弦進行與節奏
    from generate_chords import get_chord_progression
    chords_list, rhythm_pattern = get_chord_progression(style_name)

    # 2. chord_symbols 為每小節一個和弦 (Melody RNN 支援這種對應)
    chord_symbols = chords_list  # 不需展開成每拍

    # 3. 計算總小節數 (每個和弦視為一個小節)
    num_bars = len(chord_symbols)

    # 4. 建立 primer sequence
    primer = NoteSequence()
    primer.tempos.add(qpm=tempo)

    # 5. 計算生成時長 (每小節4拍)
    seconds_per_beat = 60.0 / tempo
    seconds_per_bar = seconds_per_beat * 4  # 4拍一小節
    total_seconds = num_bars * seconds_per_bar

    # 6. 設定 generator options
    gen_options = generator_pb2.GeneratorOptions()
    section = gen_options.generate_sections.add()
    section.start_time = 0
    section.end_time = total_seconds
    gen_options.args['chords'].string_value = ','.join(chord_symbols)

    # 7. 呼叫模型生成旋律
    melody_sequence = _generator.generate(primer, gen_options)
    return melody_sequence