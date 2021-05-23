from .models import UserModel

def check_user_login(email):
    return False


def id_creator(username):
    # created_slug=''
    try:
        lastuser=UserModel.objects.last()
        created_slug=str(username)+str(lastuser.id+1)
        print(created_slug)
        return created_slug
    except:
        return "abc1"
