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
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a["users"]
    print("session 1  = " + str(a))
    a = a[0]
    a = a["localId"] # on recupere localId
    print("session 2  = " + str(a))

    # intruction pour recuprer le nom d'utilisateur
    b = database.child("users").child(a).get()
    b = b[0]
    b = b.val()
    nom = b["nom"]
    tel = b["tel"]
    print("HUM = " + str(tel))
    # notre objet ann
    ann = fonction.AfficherAnnonce()
    com_list = ann.afficher(database)

    return render(request, "welcom.html", {"com_list": com_list, "e": nom})


def logout(request):

    auth.logout(request)
    return render(request, "signIn.html")

# pour se connecter
def signup(request):

    return render(request, "signup.html")

# pour se signup
def postsignup(request):

    name = request.POST.get("name")
    tel = request.POST.get("tel")
    av = request.POST.get("av")
    email = request.POST.get("email")
    passw = request.POST.get("password")

    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "impossible de creer un utilisateur essayer encore"
        return  render(request, "signup.html", {"msg": message})

    uid = user['localId']
    data = {"nom": name, "tel": tel, "av": av, "statut": "1","uid":uid}
    database.child("users").child(uid).child("details").set(data)
    # intruction pour recuprer le nom d'utilisateur
    b = database.child("users").child(uid).get()
    b = b[0]
    b = b.val()
    b = b["nom"]
    message = "utilisateur a ete cree"
    # notre objet ann
    ann = fonction.AfficherAnnonce()
    com_list = ann.afficher(database)
    return render(request, "welcom.html",  {"com_list": com_list, "msge": message, "e": b})

def create_annonce(request):

    import time
    from datetime import datetime, timezone
    import pytz
    # la date de la publication
    tz = pytz.timezone('Europe/Berlin')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    titre = request.POST.get("titre")
    cat = request.POST.get("cat")
    descp = request.POST.get("descp")
    lieu = request.POST.get("lieu")


    # intrcution pour recupere l'id dans la session
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a["users"]
    print("session 1  = " + str(a))
    a = a[0]
    a = a["localId"]
    print("session 2  = "+ str (a))

    # intruction pour recuprer le nom d'utilisateur
    b = database.child("users").child(a).get()
    b = b[0]
    b = b.val()
    nom = b["nom"]
    tel = b["tel"]
    print("HUM =  " + str(b))
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

