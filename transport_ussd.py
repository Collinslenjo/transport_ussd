import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/transport'
db = SQLAlchemy(app)

response = ""


@app.route('/', methods = ['GET','POST'])
def ussd():
    global response
    session_id = request.values.get("sessionId",None)
    service_code =  request.values.get("serviceCode",None)
    phone_number = request.values.get("phoneNumber",None)
    text = request.values.get("text",None)
    print(session_id, service_code, phone_number, text)

    if text == "" or text is None:
        response = "CON Please enter amount to deposit\n"
    else:
        response = "END Your deposit was captured successfully"
        save_conductor_deposit(service_code, session_id, phone_number,
                               int(text))

    return response


def save_conductor_deposit(service_code, session_id, phone_number,
                           deposit_amount):
    """save the offload"""
    sql = f"insert into tbl_conductor_offloads(status,service_code,session_id,phone_number,amount,date_created,date_modified)"\
          f" values( 'created',{service_code},{session_id},{phone_number},{deposit_amount},'{datetime.datetime.now()}','{datetime.datetime.now()}')"
    db.engine.execute(text(sql))


if __name__ == "__main__":
    app.run("0.0.0.0", 8090, debug=True)