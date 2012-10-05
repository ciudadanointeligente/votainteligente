# -*- coding: utf-8 -*-

from models import Pregunta, Candidato
# from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django import forms
from captcha.fields import ReCaptchaField

class PreguntaForm(forms.ModelForm):
    captcha = ReCaptchaField(attrs={'theme' : 'clean','lang':'es'})
    class Meta:
        model = Pregunta

    # Representing the many to many related field in Pizza
    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
    	comuna = kwargs['comuna']
    	del kwargs['comuna']
    	super(PreguntaForm, self).__init__(*args, **kwargs)
    	candidatos = Candidato.objects.filter(comuna = comuna)

        self.fields['candidato'].widget = forms.CheckboxSelectMultiple()
        self.fields['candidato'].label = "Label"
        self.fields['candidato'].queryset = candidatos
        self.fields['candidato'].help_text = 'Marca sólo los candidatos a los que quieras preguntar'
        self.fields['candidato'].label = 'Candidatos'
        self.fields['remitente'].widget.attrs['class'] = 'itemCandidato'
        self.fields['remitente'].help_text = 'Identifícate como quieras'
        self.fields['remitente'].initial = 'Comunero, Profesora, Dirigente, etc.'
        self.fields['remitente'].label = 'Yo soy'
        self.fields['texto_pregunta'].initial = 'Escribe una pregunta clara y respetuosa. Así aumentas la posibilidad de que respondan seriamente.'
        self.fields['texto_pregunta'].label = 'Escribe tu pregunta'

'''	
    # Overriding save allows us to process the value of 'toppings' field    
    def save(self, commit=True):
	#Recuperar los datos
	#pregunta = pregunta_form.save(commit = False)
        instance = ModelForm.save(self, False)

	#Crear respuestas
	for candidato_pk in self.cleaned_data['candidato']:
		candidato = Candidato.objects.filter(id=candidato_pk)
		instance.candidato_set.remove(candidato_pk)
		instance.candidato_set.add(candidato)
		
		#Crear respuesta

        # Do we need to save all changes now?
        if commit:
            instance.save()
            #self.save_m2m()

	return instance



        print 'saving'
        # Get the unsave Pizza instance
        instance = ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.candidato_set.clear()
           for candidato in self.cleaned_data['candidato']:

                instance.candidato_set.add(candidato)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
'''
