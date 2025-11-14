from flask import Flask, request, send_from_directory, render_template_string
import os
import subprocess
import zipfile

app = Flask(__name__)

# HTML da página de upload
HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>Gerador de Screenshots</title></head>
<body>
<h2>Arraste ou envie seu vídeo</h2>
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="video" accept="video/*" required><br><br>
  <input type="submit" value="Gerar Screenshots">
</form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video = request.files['video']
        video_path = "uploaded_video.mp4"
        video.save(video_path)

        # Executa o script de screenshots
        subprocess.run(['python', 'video_screenshots.py', video_path])

        # Cria ZIP da pasta de screenshots
        folder_name = video_path.replace(".mp4", "_screenshots")
        zip_name = f"{folder_name}.zip"
        with zipfile.ZipFile(zip_name, 'w') as zf:
            for file in os.listdir(folder_name):
                zf.write(os.path.join(folder_name, file), file)

        return f"""
        <h3>✅ Screenshots geradas com sucesso!</h3>
        <a href='/download/{zip_name}'>📥 Baixar ZIP com screenshots</a><br><br>
        <a href='/'>🔄 Gerar outro vídeo</a>
        """

    return render_template_string(HTML_FORM)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('.', filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)