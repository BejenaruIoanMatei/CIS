import os
from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired


base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

print("Template directory:", template_dir)
print("Template directory exists:", os.path.exists(template_dir))

app = Flask(__name__, template_folder=template_dir)

app.config['SECRET_KEY'] = 'afavrv'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(base_dir, 'uploads')

os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
    
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    
    if os.path.exists(template_dir):
        print("Templates in folder:", os.listdir(template_dir))
    
    return render_template('index.html', form=form, file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)