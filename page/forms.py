import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Firma,Sube,Icmal,Donem
from.models import AYLAR,YILLAR

FİRMALAR = Firma.objects.all()
SUBELER =Sube.objects.all()
ICMALLER = Icmal.objects.all()
KULLANICILAR = User.objects.all()


class KullaniciDonemForm(forms.ModelForm):
    kullanici = forms.ModelChoiceField(
        queryset=KULLANICILAR,
        required=False
    )
    ay = forms.ChoiceField(
        choices=AYLAR,
        widget=forms.Select(
        attrs={
        'class':'form-control'
        }
        )
    )
    yil = forms.ChoiceField(
        choices=YILLAR,
        widget=forms.Select(
        attrs={
        'class':'form-control'
        }
        )
    )
    class Meta:
        model = Donem
        fields = ('ay','yil',"kullanici")
 



class DonemForm(forms.Form):
    ay = forms.ChoiceField(
        choices=AYLAR,
        widget=forms.Select(
        attrs={
        'class':'form-control'
        }
        )
    )
    yil = forms.ChoiceField(
        choices=YILLAR,
        widget=forms.Select(
        attrs={
        'class':'form-control'
        }
        )
    )




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
    kdv = forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control ',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    kdv2=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    atak=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    yasalKdv=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    muhtasar=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    ggkv=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    damga=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    mtv=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    ceza=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    idariceza=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    davagideri=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    hakemheyeti=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    geçmişborçlar=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    tesvik=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    müsavirlik=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    harcama=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    sgk=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    bagkur=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    tasdik=forms.DecimalField(
            widget= forms.NumberInput(
                attrs={
                'class':'form-control',
                'placeholder':'0,00',
                'step': "0.01",
                'value': 0
                }
            ) 
    )
    sgkYapilandirmasi=forms.DecimalField(
        widget= forms.NumberInput(
            attrs={
            'class':'form-control',
            'placeholder':'0,00',
            'step': "0.01",
            'value': 0
            }
        ) 
    )
    vergiYapilandirmasi=forms.DecimalField(
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
        fields = ("sgkYapilandirmasi","vergiYapilandirmasi","tasdik",'kdv','kdv2','atak','yasalKdv','muhtasar','ggkv','damga','mtv','ceza','idariceza','davagideri','hakemheyeti','geçmişborçlar','tesvik','müsavirlik','harcama','sgk','bagkur')



