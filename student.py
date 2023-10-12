from dbsetting import *
from flask import abort
from werkzeug.debug import get_current_traceback
import json 
from datetime import datetime

# Initializing our database
db = SQLAlchemy(app)

#ORM class == table in testdatabase.db
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gpa = db.Column(db.Float)
    dob = db.Column(db.Date)
    phone = db.Column(db.String(10))

    # this method we are defining will convert our output to json
    def json(self):
        return {'id': self.id, 'name': self.name,
                'gpa': self.gpa, 'phone': self.phone, 'dob':self.dob}

    # this method will display all student records-SELECT * FROM student;
    def get_all_student():
        return [Student.json(std) for std in Student.query.all()]
        
    # this method will display student record by id-SELECT * FROM student WHERE id = _id;
    def get_student(_id):
        return [Student.json(Student.query.filter_by(id=_id).first())] #id is unique because id is primary key
    
    def get_studentbyname(_name):
        return [Student.json(Student.query.filter_by(name=_name).first())]
    
    def update_studentgpa(_id,_gpa):
        student_update=Student.query.filter_by(id=_id).first()
        student_update.gpa=_gpa
        db.session.commit()
    
    # this method will insert new student record INSERT INTO 
    def add_student(_id, _name, _gpa, _phone, _dob):
        new_student = Student(id=_id,name=_name,gpa=_gpa,phone=_phone,dob=_dob)
        db.session.add(new_student)
        db.session.commit()

@app.route('/api', methods=['POST'])
def add_student():
    request_data = request.get_json()
    date_obj = datetime.strptime(request_data["dob"],"%Y-%m-%d") #1990-10-05
    Student.add_student(request_data["id"],request_data["name"],request_data["gpa"],request_data["phone"],date_obj)
    response = Response("Student record already added",status=201,mimetype='application/json')
    return response

@app.route('/api/<int:id>', methods=['PUT','PATCH'])
def update_gpa(id):
    try:
        return_value=Student.get_student(id)
        if (return_value):
            request_data = request.get_json()
            Student.update_studentgpa(id,request_data['gpa'])
            response = Response("Student's GPA is updated", status=200, mimetype='application/json')
            return response
    except Exception:
        track=get_current_traceback(skip=1, show_hidden_frames=True,ignore_system_exceptions=False)
        track.log()
        abort(500)


@app.route('/api',methods=['GET'])
def show_allstudent():
    return jsonify(Student.get_all_student())
    #return render_template('show_allstudent.html', students=Student.get_all_student())

@app.errorhandler(500)
def internal_error(error):
    response = Response("Student Record Not Found!!", status=500, mimetype='application/json')
    return response
    #return render_template('show_allstudent.html', students="")

# route to get student by id
@app.route('/api/<int:id>', methods=['GET'])
def get_student_by_id(id):
    try:
        return_value = Student.get_student(id) # return = none, null
        if (return_value):
            return jsonify(return_value)
            #return render_template('show_allstudent.html', students=return_value)
    except Exception:
        track=get_current_traceback(skip=1, show_hidden_frames=True,ignore_system_exceptions=False)
        track.log()
        abort(500)

# route to get student by name
@app.route('/api/<string:name>', methods=['GET'])
def get_student_by_name(name):
    try:
        return_value = Student.get_studentbyname(name) # return = none, null
        if (return_value):
            return jsonify(return_value)
            #return render_template('show_allstudent.html', students=return_value)
    except Exception:
        track=get_current_traceback(skip=1, show_hidden_frames=True,ignore_system_exceptions=False)
        track.log()
        abort(500)

if __name__ == "__main__":
    app.run(port=1234, debug=True)    