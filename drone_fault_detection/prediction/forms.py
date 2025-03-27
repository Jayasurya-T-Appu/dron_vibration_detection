from django import forms

class SensorInputForm(forms.Form):
    sensor_a = forms.FloatField(label="Sensor A")
    sensor_b = forms.FloatField(label="Sensor B")
    sensor_c = forms.FloatField(label="Sensor C")
    sensor_d = forms.FloatField(label="Sensor D")
