from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Firma,Girdi,Sube,YEAR_CHOICES,MONTH_CHOICES,Icmal

FİRMALAR = Firma.objects.all()
SUBELER =Sube.objects.all()
ICMALLER = Icmal.objects.all()

def firmaSec(firma):
    subeler = Sube.objects.filter(firma=firma)
    return subeler

class IcmalBir(forms.Form):
    sube = forms.ModelChoiceField(
        FİRMALAR,
            widget=forms.Select(
                attrs={
                'class':'form-control ',
                'placeholder':'Firma Seçiniz'
                    }
                )
    )

class IcmalUc(forms.Form):
    sube = forms.ModelChoiceField(
        SUBELER,
            widget=forms.Select(
                attrs={
                'class':'form-control ',
                'placeholder':'Şube Seçiniz'
                    }
                )
    )


class SgkForm(forms.ModelForm):
    sgk = forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control ',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    tesvik = forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control ',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    class Meta:
        model = Icmal
        fields = ('sgk', 'tesvik')


class HizliForm(forms.Form):
    firma = forms.ModelChoiceField(
        FİRMALAR,
            widget=forms.Select(
                attrs={
                'class':'form-control ',
                'placeholder':'Firma Seçiniz'
                    }
                )
    )

    

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adınız'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Soyadınız'
        })
    )
    username = forms.CharField(
        max_length = 100,
        required=True,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adınız'
        })
    )
    email = forms.EmailField(
        max_length=254,
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mailiniz'
        })
    )
    password1 = forms.CharField(
    max_length = 100,
    required=True,
    widget = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parola'
        })
    )
    password2 = forms.CharField(
    max_length = 100,
    required=True,
    widget = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolanızı Doğrulayın'
        })
    )

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email','username', 'password1', 'password2')




class SignInForm(forms.Form):

    username = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Kullanıcı Adınız:'
        })
    )
    password = forms.CharField(
    required=True,
    widget = forms.PasswordInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Parola:'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class FirmaCreateForm(forms.Form):
    isim = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-3',
                'placeholder' : 'Firma ismi..'
            })
        )
    sube = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-3',
                'placeholder' : 'Sube ismi..'
            })
        )
    sgkNo =forms.IntegerField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control mb-1',
                'placeholder':'Sgk No:',                
                }
            ))   



class FirmaForm(forms.ModelForm):
    isim = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-3',
                'placeholder' : 'Firma ismi..'
            })
        )
    class Meta:
        model = Firma
        fields = ("isim",)


class SubeForm(forms.ModelForm):
    isim = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-3',
                'placeholder' : 'Sube ismi..'
            })
        )
    firma = forms.ModelChoiceField(FİRMALAR,
    widget=forms.Select(
        attrs={
            'class':'form-control my-3',
            'placeholder' : 'Firma Seçiniz'
        }
    )
    )
    sgkNo =forms.IntegerField(required=False,
            widget= forms.TextInput(
                attrs={
                "pattern":"\d*",
                "maxlength": "26",
                'class':'form-control mb-1',
                'placeholder':'Sgk No:',                
                }
            ))
    class Meta:
        model = Sube
        fields = ("isim",'firma',"sgkNo")


class GirdiForm(forms.ModelForm):
    kdv = forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control ',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    kdv2=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    atak=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    yasalKdv=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    muhtasar=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    ggkv=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    damga=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    mtv=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    ceza=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    idariceza=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    davagideri=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    hakemheyeti=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    geçmişborçlar=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    tesvik=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    müsavirlik=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    harcama=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    sgk=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    bagkur=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    tasdik=forms.DecimalField(required=False,
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )

    class Meta:
        model = Icmal
        fields = ("tasdik",'kdv','kdv2','atak','yasalKdv','muhtasar','ggkv','damga','mtv','ceza','idariceza','davagideri','hakemheyeti','geçmişborçlar','tesvik','müsavirlik','harcama','sgk','bagkur')




class OdemeIcmaliForm(forms.Form):
    satır = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control col-5',
                
            }
        )
    )
    def __init__(self, *args, **kwargs):
        super(OdemeIcmaliForm, self).__init__(*args, **kwargs)
        self.fields['satır'].required = False
