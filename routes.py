from flask import Blueprint, render_template, request, redirect, url_for
from pydantic import ValidationError
import json

from extensions import db
from models import DataEntry
from schemas import JsonItem

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/upload', methods=['GET', 'POST'])
def upload_json():
    if request.method == 'GET':
        return render_template('upload.html')

    file = request.files.get('file')
    if not file:
        return render_template('upload.html', errors=['Файл не выбран'])

    try:
        file_content = file.read().decode('utf-8')
        json_data = json.loads(file_content)

        if not isinstance(json_data, list):
            return render_template('upload.html', errors=['JSON должен быть массивом объектов'])

        valid_items = []
        all_errors = []

        for index, item in enumerate(json_data):
            if not isinstance(item, dict):
                all_errors.append(f"Элемент №{index + 1}: должен быть объектом (словарем)")
                continue

            try:
                valid_item = JsonItem.model_validate(item)
                valid_items.append(valid_item)
            except ValidationError as e:
                for err in e.errors():
                    field_name = err['loc'][0]  # Название упавшего поля (name или date)
                    error_msg = err['msg']  # Сообщение об ошибке от Pydantic
                    all_errors.append(f"Элемент №{index + 1}, поле '{field_name}': {error_msg}")

        if all_errors:
            return render_template('upload.html', errors=all_errors)

    except json.JSONDecodeError:
        return render_template('upload.html', errors=['Неверный формат JSON (синтаксическая ошибка)'])
    except UnicodeDecodeError:
        return render_template('upload.html', errors=['Файл должен быть в кодировке UTF-8'])

    db.session.add_all(
        DataEntry(name=item.name, date=item.date)
        for item in valid_items
    )
    db.session.commit()

    return redirect(url_for('main.entries'))


@main_bp.route('/entries')
def entries():
    all_entries = DataEntry.query.all()
    return render_template('entries.html', entries=all_entries)