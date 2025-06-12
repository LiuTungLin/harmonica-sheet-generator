from flask import Flask, render_template_string, request, send_from_directory
import os
import datetime
from note_seq import sequence_proto_to_midi_file
from note_seq.protobuf import music_pb2
from generate_melody import generate_melody
from generate_bass import generate_bass
from generate_chords import get_chord_progression, generate_chords
from style_mapper import map_style

app = Flask(__name__)

# MIDI 輸出資料夾（專案根目錄下 midis）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MIDIS_DIR = os.path.join(BASE_DIR, 'midis')
os.makedirs(MIDIS_DIR, exist_ok=True)

# HTML 模板（使用 Bootstrap）
TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MIDI 產生器</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">MIDI 產生器</a>
    </div>
  </nav>
  <div class="container py-4">
    <div class="row">
      <div class="col-md-8">
        <h2>專案介紹</h2>
        <p>本專案提供一個三重奏樂譜的生成工具，使用者可以輸入音樂風格與速度(BPM)，系統會輸出一個包含主旋律、和弦、低音的三軌 MIDI 檔案。</p>
      </div>
      <div class="col-md-4">
        <form method="post" action="/generate">
          <div class="mb-3">
            <label class="form-label">自訂風格描述</label>
            <input type="text" class="form-control" name="user_desc" placeholder="輸入風格，如：藍調爵士">
          </div>
          <div class="mb-3">
            <label class="form-label">或選擇預設風格</label>
            <select class="form-select" name="style">
              {% for s in styles %}
                <option value="{{ s }}" {% if s==selected_style %}selected{% endif %}>{{ s }}</option>
              {% endfor %}
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">節奏 (BPM)</label>
            <input type="number" class="form-control" name="tempo" value="{{ tempo }}" min="30" max="300">
          </div>
          <button type="submit" class="btn btn-primary w-100">生成 MIDI</button>
        </form>
        {% if filename %}
        <div class="alert alert-success mt-3">
          已生成：<a href="/midis/{{ filename }}" target="_blank">{{ filename }}</a><br>
          {% if mapped %}映射風格：{{ mapped }} (相似度：{{ score }}){% endif %}
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</body>
</html>
'''

# 內建風格列表
PREDEFINED_STYLES = [
    "Modern", "Ashanti", "Ewe", "Funk", "Ballad",
    "Reggae", "Rock", "Disco", "Pop", "Blues",
    "Jazz", "Hiphop", "Samba", "Tango", "Folk"
]

@app.route('/', methods=['GET'])
def index():
    return render_template_string(
        TEMPLATE,
        styles=PREDEFINED_STYLES,
        selected_style="Folk",
        tempo=120,
        filename=None
    )

@app.route('/generate', methods=['POST'])
def generate():
    user_desc = request.form.get('user_desc', '').strip()
    if user_desc:
        style, score = map_style(user_desc)
        mapped = style
        score = f"{score:.2f}"
    else:
        style = request.form.get('style', 'Folk')
        mapped = None
        score = None
    try:
        tempo = int(request.form.get('tempo', 120))
    except ValueError:
        tempo = 120

    # 生成 MIDI
    chords_list, rhythm_pattern = get_chord_progression(style)
    melody_seq = generate_melody(style, tempo)
    bass_seq = generate_bass(style, tempo)
    chords_seq = generate_chords(chords_list, rhythm_pattern, tempo)
    merged = music_pb2.NoteSequence()
    for seq in [melody_seq, bass_seq, chords_seq]:
        merged.notes.extend(seq.notes)
        merged.text_annotations.extend(seq.text_annotations)
        merged.total_time = max(merged.total_time, seq.total_time)
    merged.tempos.add(qpm=tempo)

    filename = f"harmonica_sheet_{datetime.datetime.now():%Y%m%d%H%M}_{style}.mid"
    out_path = os.path.join(MIDIS_DIR, filename)
    sequence_proto_to_midi_file(merged, out_path)

    return render_template_string(
        TEMPLATE,
        styles=PREDEFINED_STYLES,
        selected_style=style,
        tempo=tempo,
        filename=filename,
        mapped=mapped,
        score=score
    )

@app.route('/midis/<path:filename>')
def download_midi(filename):
    return send_from_directory(MIDIS_DIR, filename, as_attachment=True)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
