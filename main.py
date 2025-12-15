import io
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime 
from flask_restful import Api
from flask import Flask, render_template, redirect, url_for, request, abort, session, jsonify
from werkzeug.serving import WSGIRequestHandler
from utils import *

from data import db_session
from data.applications import Applications
from data.rooms import Rooms
from data.floors import Floors
from data.photos import Photos
from data.statuses import Statuses

app = Flask(__name__)
app.config["SECRET_KEY"] = "Bebrochka666"
app.config['UPLOAD_FOLDER'] = 'uploads'

api = Api(app)

db_session.global_init('db/applications.db')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/add_application', methods=['GET', 'POST'])
def add_application():
    if request.method == "POST":
        fullName = request.form.get("fullName")
        phoneNumber = request.form.get("phoneNumber")
        roomNumber = request.form.get("roomNumber")
        issueDescription = request.form.get("issueDescription")
        notify = bool(request.form.get("notify"))
        
        session = db_session.create_session();
        cur_date = datetime.now()
        application = Applications(
            status_id = 1,
            created_at = cur_date,
            phoneNumber = phoneNumber,
            name = fullName,
            room_id = session.query(Rooms).filter(Rooms.room == roomNumber).first().id,
            description = issueDescription,
            notify = notify
        )
        session.add(application)
        session.flush();

        today = cur_date
        year = str(today.year)
        month = str(today.month).zfill(2)
        day = str(today.day).zfill(2)
        
        upload_dir = '/'.join([
            'static',
            app.config['UPLOAD_FOLDER'],
            'applications',
            year,
            month,
            day])
        os.makedirs(upload_dir, exist_ok=True)

        files = request.files.getlist('photos')
        for index, file in enumerate(files):
            if file and file.filename:
                original_name = secure_filename(file.filename)
                file_ext = os.path.splitext(file.filename)[1]
                unique_name = f"{application.id}_{uuid.uuid4().hex}{file_ext}"
                original_path = '/'.join([upload_dir, unique_name])
                file.save(original_path)
                thumb_path = '/'.join([upload_dir, f"thumb_{unique_name}"])
                create_thumbnail(original_path, thumb_path, size=(150, 150))
                photo = Photos(
                    application_id=application.id,
                    filename=original_name,
                    filepath='/'.join([app.config['UPLOAD_FOLDER'], 'applications', year, month, day, unique_name]),
                    thumbnail_path='/'.join([app.config['UPLOAD_FOLDER'], 'applications', year, month, day, f"thumb_{unique_name}"]),
                    order=index
                )
                session.add(photo)
        session.commit()
        
        photos = session.query(Photos).filter(Photos.application_id == application.id).order_by(Photos.order).all()
        app_ = {
                "id": application.id,
                "status": session.query(Statuses).filter(application.status_id == Statuses.id).first().status,
                "created_at": application.created_at,
                "phoneNumber": application.phoneNumber,
                "name": application.name,
                "room": session.query(Rooms).filter(application.room_id == Rooms.id).first().room,
                "floor": session.query(Floors).filter(session.query(Rooms).filter(application.room_id == Rooms.id).first().floor_id == Floors.id).first().floor,
                "description": application.description,
                "notify": application.notify,
            }
        return render_template('application_preview.html', application=app_, photos=photos)
    return render_template('application_form.html')


@app.route('/apps_panel', methods=['GET'])
def apps_panel():
    session = db_session.create_session()

    total = session.query(Applications).all()
    new = session.query(Applications).filter(Applications.status_id == 1).all()
    in_progress = session.query(Applications).filter(Applications.status_id == 2).all()
    completed = session.query(Applications).filter(Applications.status_id == 3).all()
    stats = {'new': len(new), 'in_progress': len(in_progress), 'completed': len(completed), 'total': len(total)}

    applications = []
    for app_ in total:
        applications.append({
            "id": app_.id,
            "status": session.query(Statuses).filter(app_.status_id == Statuses.id).first().status,
            "created_at": app_.created_at,
            "phoneNumber": app_.phoneNumber,
            "name": app_.name,
            "room": session.query(Rooms).filter(app_.room_id == Rooms.id).first().room,
            "floor": session.query(Floors).filter(session.query(Rooms).filter(app_.room_id == Rooms.id).first().floor_id == Floors.id).first().floor,
            "description": app_.description,
            "notify": app_.notify,
        })

    param = {'stats': stats, 'applications': applications}

    return render_template('application_panel.html', **param)


@app.route('/application/<int:id>', methods=['GET'])
def application_preview(id):
    session = db_session.create_session()
    app_ = session.query(Applications).filter(Applications.id == id).first()
    if not app_:
        session.close()
        return "Заявка не найдена", 404

    photos = session.query(Photos).filter(Photos.application_id == id).order_by(Photos.order).all()
    for photo in photos:
        print(photo.filepath)
    application = {
            "id": app_.id,
            "status": session.query(Statuses).filter(app_.status_id == Statuses.id).first().status,
            "created_at": app_.created_at,
            "phoneNumber": app_.phoneNumber,
            "name": app_.name,
            "room": session.query(Rooms).filter(app_.room_id == Rooms.id).first().room,
            "floor": session.query(Floors).filter(session.query(Rooms).filter(app_.room_id == Rooms.id).first().floor_id == Floors.id).first().floor,
            "description": app_.description,
            "notify": app_.notify,
        }
    
    return render_template('application_admin_preview.html', application=application, photos=photos)
    

@app.route('/application/<int:id>', methods=['DELETE'])
def delete_application(id):
    session = db_session.create_session()
    app_ = session.query(Applications).filter(Applications.id == id).first()
    if app_:
        for photo in session.query(Photos).filter(Photos.application_id == app_.id).all():
            os.remove('static/' + photo.filepath)
            os.remove('static/' + photo.thumbnail_path)
            session.delete(photo)
        session.delete(app_)
        session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Заявка не найдена'})


@app.route('/application/<int:id>/status', methods=['PUT'])
def update_application_status(id):
    data = request.get_json()
    new_status = data.get('status')
    
    session = db_session.create_session()
    app_ = session.query(Applications).filter(Applications.id == id).first()

    status = ''
    
    if app_ and new_status in ['new', 'in_progress', 'completed']:
        if new_status == 'new': status = 'Новый запрос'
        elif new_status == 'in_progress': status = 'В обработке'
        elif new_status == 'completed': status = 'Завершено'
        app_.status_id = session.query(Statuses).filter(Statuses.status == status).first().id
        session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Ошибка'})


def main():
    session = db_session.create_session()
    session.commit()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
