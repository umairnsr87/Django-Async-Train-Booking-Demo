from time import sleep
from .models import Train, Booking
import datetime
from test_tft.celery import app


@app.task
def check_train(**kwargs):
    try:
        train = Train.objects.get(source=kwargs["source"], destination=kwargs["destination"])
        chain = check_status.s(kwargs["date"]) | check_seats.s(kwargs["passengers"], train.capacity
                                                               , id=kwargs["id_train"], train_name=train.name,
                                                               train_id=train.id)
        chain()

        # return train.capacity,train.name,train.id
    except:
        return False


@app.task
def check_status(date):
    if datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") < datetime.datetime.now():
        return 0
    else:
        return 1


@app.task
def check_seats(x, seats, available_seats, id, train_name, train_id):
    if x == 1:
        if available_seats - seats >= 0:
            print("slept for 50 seconds")
            sleep(30)
            x = Booking.objects.filter(id=id).update(status=True, train_name=train_name, train_id=train_id)
        # return 1

# @app.task
# def update_booking_status(status1, status2, id, train_name, train_id):
#     if (status1 and status2)==1:
#         print("slept for 50 seconds")
#         sleep(50)
#         x=Booking.objects.filter(id=id).update(status=True,train_name=train_name,train_id=train_id)
#         # return 1
#     else:
#         pass
