from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters."
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if User.objects.filter(email=postData['email']).exists():
            errors["email"] = "Email already exists."
        return errors

    def login_validator(postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "Please provide an email address."
        if len(postData['password']) < 1:
            errors["password"] = "Please provide a password."
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "The email address you've entered is invalid."
        else:
            user = User.objects.filter(email=postData['email']).first()
            if not user:
                errors["email"] = "No user account with this email address was found. Please register."
            else:
                if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    errors["password"] = "Incorrect password."
        return errors

    def add_user(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        self.create(
            fname=data['fname'],
            lname=data['lname'],
            email=data["email"],
            password=hashed_password,
        )

class PieManager(models.Manager):
    def pie_validator(self, postData):
        errors = {}
        if len(postData['piename']) < 2:
            errors["piename"] = "Pie name can't be empty."
        if len(postData['filling']) < 2:
            errors["filling"] = "Please include the filling."
        if len(postData['crust']) < 2:
            errors["crust"] = "Please include the crust."
        return errors

    def add_pie(self, data, user_id):
        user = User.objects.get(id=user_id)
        return self.create(
            piename=data['piename'],
            filling=data['filling'],
            crust=data['crust'],
            vote=0,
            baker=user,
        )

    
    
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Pie(models.Model):
    piename = models.CharField(max_length=50)
    filling = models.CharField(max_length=50)
    crust = models.CharField(max_length=50)
    vote = models.SmallIntegerField()
    baker = models.ForeignKey(User ,related_name="pie" , on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PieManager()
    

def get_all_pie():
    return Pie.objects.all()


