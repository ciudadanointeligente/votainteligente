from models import Pregunta, Candidato
from django.forms import ModelForm, ModelMultipleChoiceField

class PreguntaForm(ModelForm):
    class Meta:
        model = Pregunta

    # Representing the many to many related field in Pizza
    candidato = ModelMultipleChoiceField(queryset=Candidato.objects.all())
    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
	comuna = kwargs['comuna']
	del kwargs['comuna']
	super(PreguntaForm, self).__init__(*args, **kwargs)
	#Falta filtrar los candidatos por comuna
	candidatos = Candidato.objects.filter(comuna = comuna)
	self.fields['candidato'].queryset = candidatos

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
