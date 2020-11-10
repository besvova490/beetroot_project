from flask import jsonify


class BaseFuncs:

    @staticmethod
    def get_obj(obj_class, obj_id):
        return obj_class.query.get(obj_id)

    @staticmethod
    def get_obj_dict_or_404(obj_class, obj_id, **kwargs):
        obj = obj_class.query.get(obj_id, **kwargs)
        if obj:
            return jsonify({'item': obj.to_dict()}), 200
        return jsonify({'msg': 'object is not found'}), 404

    @staticmethod
    def get_objects_dict_list_or_404(obj_class, **kwargs):
        objects_list = [obj.to_dict() for obj in obj_class.query.filter_by(**kwargs) if obj]
        if objects_list:
            return jsonify({'items': objects_list}), 200
        return jsonify({'msg': 'objects is not found'}), 404

    @staticmethod
    def delete_object(obj, db):
        try:
            db.session.delete(obj)
            db.session.commit()
            return jsonify({'msg': 'Obj deleted'}), 201
        except Exception as e:
            return jsonify({'msg': e}), 404

    @staticmethod
    def update_obj(obj_class, obj_id, db, data):
        try:
            if 'id' in data:
                return jsonify({'msg': 'Invalid data'}), 400
            obj_class.query.filter_by(id=obj_id).update(data)
            db.session.commit()
            return jsonify({'msg': 'Updated successful'}), 201
        except Exception as e:
            return jsonify({'msg': e}), 404
