from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()


class Streets(models.Model):
    street_name = models.CharField(max_length=50)


class Routes(models.Model):
    time_departure = models.TimeField()
    time_arrive = models.TimeField()
    route_owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    streets = models.ManyToManyField(Streets, through='Route_Street')


class Route_Street(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)
    street = models.ForeignKey(Streets, on_delete=models.CASCADE)


class Dialog(models.Model):
    dialog_name = models.CharField(max_length=40)


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)


class R_S_Person(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    R_S = models.ForeignKey(Route_Street, on_delete=models.CASCADE)


mods = {'dms_person': Person, 'dms_streets': Streets, 'dms_routes': Routes, 'dms_route_street': Route_Street,
        'dms_dialog': Dialog, 'dms_message': Message, 'dms_r_s_person': R_S_Person}
