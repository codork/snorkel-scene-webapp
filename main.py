import os
#from flask_opencv_streamer.streamer import Streamer
import cv2
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, Response, send_file
from werkzeug.utils import secure_filename
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import pandas as pd
import shutil



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
test_datagen = ImageDataGenerator(rescale=1 / 255.0)
model = load_model('./models/model_1.h5')
rev_scene_categories_dict={0:'bathroom', 1:'beach', 2:'bedroom', 3:'cottage', 4:'forest_road', 5:'hayfield', 6:'kitchen', 7:'playground'}
CATEGORIES = list(rev_scene_categories_dict.values())

project_dir = os.getcwd()
STATIC_FOLDER = project_dir + '\static'
DOWNLOAD_FOLDER = os.path.join(project_dir, 'static\download')

#DOWNLOAD_FOLDER = r'D:\Project\data-labelling-webapp-single_multiple_css_reloading\static\download'
#STATIC_FOLDER = r'D:\Project\data-labelling-webapp-single_multiple_css_reloading\static'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/label-single', methods=['POST', 'GET'])
def upload_single_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash(filename)

		predicted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

		image = cv2.imread(predicted_image_path)
		predicted_label = -1
		list_pred = [[predicted_image_path, predicted_label]]
		pred_df = pd.DataFrame(list_pred, columns = ['path', 'label'])
		inf_datagen = ImageDataGenerator(rescale=1 / 255.0)
		inf_generator = inf_datagen.flow_from_dataframe(
			dataframe=pred_df,
			x_col="path",
			target_size=(256, 256),
			batch_size=1,
			class_mode=None,
			shuffle=False,
		)
		predicted_label = model.predict_generator(inf_generator).argmax(axis=-1)
		prediction_category = rev_scene_categories_dict[predicted_label[0]]

		prediction ={
			'predicted_label': predicted_label,
			'prediction_category': prediction_category
		}
		return render_template('index.html', filename=filename, result=prediction['prediction_category'])
	else:
		flash('Allowed image types are -> png, jpg, jpeg')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/label-multiple', methods=['POST'])
def upload_multiple_images():
	# Create dir structure
	if 'download' not in os.listdir(STATIC_FOLDER): # 'D:\Project\snorkel-labeller-webapp\static'):
		os.mkdir(DOWNLOAD_FOLDER)
		for cat in CATEGORIES:		
			os.mkdir(os.path.join(DOWNLOAD_FOLDER, cat))

	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			predicted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			image = cv2.imread(predicted_image_path)
			predicted_label = -1
			list_pred = [[predicted_image_path, predicted_label]]
			pred_df = pd.DataFrame(list_pred, columns = ['path', 'label'])
			inf_datagen = ImageDataGenerator(rescale=1 / 255.0)
			inf_generator = inf_datagen.flow_from_dataframe(
			dataframe=pred_df,
			x_col="path",
			target_size=(256, 256),
			batch_size=1,
			class_mode=None,
			shuffle=False,
			)
			predicted_label = model.predict_generator(inf_generator).argmax(axis=-1)
			prediction_category = rev_scene_categories_dict[predicted_label[0]]
			prediction ={
			'predicted_label': predicted_label,
			'prediction_category': prediction_category
			}
			flash(filename)  
			result=prediction['prediction_category']
			shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(DOWNLOAD_FOLDER, prediction_category))
		else:
			flash('Allowed image types are -> png, jpg, jpeg')
			return redirect(request.url)
	return render_template('index.html', filenames=file_names)

	
@app.route('/download')
def download_zip():
	if 'download.zip' in 'D:\Project\data-labelling-webapp-single_multiple_css_reloading\static':
		os.remove('D:\Project\data-labelling-webapp-single_multiple_css_reloading\static\download.zip')
	os.chdir(STATIC_FOLDER)
	zipDoc = shutil.make_archive('download', 'zip', DOWNLOAD_FOLDER)
    # Code to download
	result = send_file('D:\Project\data-labelling-webapp-single_multiple_css_reloading\static\download.zip',
                     mimetype='application/zip',
                     download_name='download.zip',
                     as_attachment=True)
	os.chdir('D:\Project\data-labelling-webapp-single_multiple_css_reloading')
	shutil.rmtree(DOWNLOAD_FOLDER)
	return result
		
if __name__ == "__main__":
    app.run()