from .models import Entry
from app import db
from flask import jsonify


class AIService:

    @staticmethod
    def hair_transplant_service(work_dict):
        service_name = 'hair_transplant'
        new_entry = Entry(service=service_name,
                          user_id=work_dict['user'],
                          image=work_dict['image'])

        db.session.add(new_entry)
        db.session.commit()

        pre_image = new_entry.image

        result = {'image': new_entry.image}

        return result

    @staticmethod
    def weight_loss_service(work_dict):
        service_name = 'weight_loss'
        new_entry = Entry(service=service_name,
                          user_id=work_dict['user'],
                          image=work_dict['image'])

        db.session.add(new_entry)
        db.session.commit()

        pre_image = new_entry.image

        result = {'image': new_entry.image}

        return result

    @staticmethod
    def muscle_gain_service(work_dict):
        service_name = 'muscle_gain'
        new_entry = Entry(service=service_name,
                          user_id=work_dict['user'],
                          image=work_dict['image'])

        db.session.add(new_entry)
        db.session.commit()

        pre_image = new_entry.image

        result = {'image': new_entry.image}

        return result




