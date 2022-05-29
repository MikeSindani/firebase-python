import datetime

from django.shortcuts import render
from django.contrib import auth
import pyrebase
from . import fonction


firebaseConfig = {
    'apiKey': "AIzaSyBuwWCDpsLuwcrygf5qGuTkiznBMjFclNA",
    'authDomain': "annoncesite-5d608.firebaseapp.com",
    'databaseURL': "https://annoncesite-5d608-default-rtdb.firebaseio.com",
    'projectId': "annoncesite-5d608",
    'storageBucket': "annoncesite-5d608.appspot.com",
    'messagingSenderId': "729688890729",
    'appId': "1:729688890729:web:30db15c91ef10f9d2e31f8",
    'measurementId': "G-E13XZ4TGFL"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
# Get a reference to the auth service
authe = firebase.auth()
database = firebase.database()


def signin(request):

    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get("email")
    passw = request.POST.get("password")

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "veillez introduire le bon mot de passe ou  nom de utilisateur"
        return render(request, "signIn.html", {"msg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    # intrcution pour recupere l'id dans la session
    geta = fonction.AfficherAnnonce()
    uid = geta.get_token(request, authe)

    # intruction pour recuprer le nom d'utilisateur

    data = geta.get_profil_data(database = database,uid = uid )
    print("HUM = " + str(data))

    # notre objet ann
    com_list = geta.afficher(database)

    return render(request, "welcom.html", {"com_list": com_list, "data":data})


def logout(request):

    auth.logout(request)
    return render(request, "signIn.html")

# pour se connecter
def signup(request):

    return render(request, "signup.html")

# pour se signup
def postsignup(request):
    #recuperer le form de signUp
    name = request.POST.get("name")
    prenom = request.POST.get("prenom")
    entreprise = request.POST.get("entreprise")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    whatsapp = request.POST.get("whatsapp")
    telegram = request.POST.get("telegram")
    adr = request.POST.get("adr")
    imgurl = request.POST.get("url")
    email = request.POST.get("email")
    passw = request.POST.get("password")


    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "impossible de creer un utilisateur essayer encore"
        return  render(request, "signup.html", {"msg": message})

    uid = user['localId']
    data = {"nom": name,"prenom":prenom ,"entreprise":entreprise,"tel1": tel1,"tel2": tel2,"whatsapp":whatsapp,"telegram":telegram, "adr": adr,"email":email,"imgurl":imgurl, "statut": "1","uid":uid}
    database.child("utilisateurs").child(uid).child("Informations").set(data)

    # intruction pour recuprer le nom d'utilisateur
    nom = database.child("utilisateurs").child(uid).child('Informations').child('nom').get().val()
    donnee = database.child("utilisateurs").child(uid).child('Informations').get().val()
    print("nom "+ nom)
    #tel = database.child("users").child(a).child('details').child('tel').get().val()

    message = "utilisateur a ete cree"
    # notre objet ann
    ann = fonction.AfficherAnnonce()
    com_list = ann.afficher(database)
    return render(request, "welcom.html",  {"com_list": com_list, "msge": message, "e": nom})



def create_annonce(request):

    import time
    from datetime import datetime, timezone
    import pytz
    # la date de la publication
    tz = pytz.timezone('Europe/Berlin')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple())) #le temps qu'on a recuperer

    # on recuper les infos du formulaires
    titre = request.POST.get("titre")
    cat = request.POST.get("cat")
    descp = request.POST.get("descp")
    lieu = request.POST.get("lieu")


    # intrcution pour recupere l'id dans la session
    geta = fonction.AfficherAnnonce()
    a = geta.get_token(request, authe)

    # intruction pour recuprer le nom d'utilisateur
    nom = database.child("users").child(a).child('details').child('nom').get().val()
    tel = database.child("users").child(a).child('details').child('tel').get().val()
    print("HUM =  " + str(nom))

    #le dictionnaire des donnes a envoyer a firebase
    data = {
        "titre": titre,
        "categorie": cat,
        "description": descp,
        "nom": nom,
        "tel": tel,
        "date pub": millis,
        "lieu": lieu,
    }
    #put data in the firedata base
    try:
            database.child("data").child("annonce").child(millis).set(data)
    except:
        message = "Annonce non publies"
        return render(request, "welcom.html", {"msge": message, "e": nom})
    message = "Annonce  publies"

    # notre objet ann
    ann = fonction.AfficherAnnonce()
    com_list = ann.afficher(database)
    return render(request, "welcom.html", {"com_list": com_list, "msge": message, "e": nom})


def post_check(request):
    import datetime
    time = request.GET.get('t')
    # instruction pour recuperer les donnes sur firebase
    titre = database.child("data").child("annonce").child(time).child('titre').get().val()
    tel = database.child("data").child("annonce").child(time).child('tel').get().val()
    cat = database.child("data").child("annonce").child(time).child('categorie').get().val()
    desc = database.child("data").child("annonce").child(time).child('description').get().val()
    nomu = database.child("data").child("annonce").child(time).child('nom').get().val()
    millis = database.child("data").child("annonce").child(time).child('date pub').get().val()

    #recupere la date pour transformer ca en date normal
    i = float(millis)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    # instruction pour recupere les donnes firebase dans un dictionnaire
    data = {
        "titre": titre,"categorie": cat,"description": desc, "nom": nomu,"tel": tel, "datepub": dat
    }

    # intrcution pour recupere l'id dans la session
    geta = fonction.AfficherAnnonce()
    a = geta.get_token(request, authe)

    # intruction pour recuprer le nom d'utilisateur
    nom = database.child("users").child(a).child('details').child('nom').get().val()
    tel = database.child("users").child(a).child('details').child('tel').get().val()
    print("HUM =  " + str(nom))



    return render( request, "description.html", {"data": data, "e": nom} )
