import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

#ที่เก็บข้อมูล
data_list = []

class Test(Resource):
    def get(self):
        """
        Test GET
        ---
        responses:
          200:
            description: A list of messages
            schema:
              properties:
                messages:
                  type: array
                  items:
                    type: string
        """
        return jsonify({'messages': data_list})

    def post(self):
        """
        Test POST
        ---
        parameters:
          - name: message
            in: formData
            type: string
            required: true
            description: The message to be posted.
        responses:
          201:
            description: Message posted successfully
            schema:
              properties:
                message:
                  type: string
                  example: Message posted successfully
        """
        try:
            message = request.form.get('message')
            data_list.append(message)
            response = {'message': f'Message posted successfully: {message}'}
            return jsonify(response), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self):
        """
        Test PUT
        ---
        parameters:
          - name: index
            in: formData
            type: integer
            required: true
            description: The index of the message to be updated.
          - name: message
            in: formData
            type: string
            required: true
            description: The updated message.
        responses:
          200:
            description: Message updated successfully
            schema:
              properties:
                message:
                  type: string
                  example: Message updated successfully
          400:
            description: Invalid index or other errors
            schema:
              properties:
                error:
                  type: string
        """
        try:
            index = int(request.form.get('index'))
            message = request.form.get('message')

            if 0 <= index < len(data_list):
                data_list[index] = message
                response = {'message': f'Message updated successfully: {message}'}
                return jsonify(response)

            return jsonify({'error': 'Invalid index'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self):
        """
        Test DELETE
        ---
        parameters:
          - name: index
            in: formData
            type: integer
            required: true
            description: The index of the message to be deleted.
        responses:
          200:
            description: Message deleted successfully
            schema:
              properties:
                message:
                  type: string
                  example: Message deleted successfully
          400:
            description: Invalid index or other errors
            schema:
              properties:
                error:
                  type: string
        """
        try:
            index = int(request.form.get('index'))

            if 0 <= index < len(data_list):
                deleted_message = data_list.pop(index)
                response = {'message': f'Message deleted successfully: {deleted_message}'}
                return jsonify(response)

            return jsonify({'error': 'Invalid index'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

api.add_resource(Test, '/Test')

swagger = Swagger(app)

if __name__ == '__main__':
    app.run(debug=True)
