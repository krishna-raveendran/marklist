from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.db import connection
import uuid
from datetime import datetime
from django.core.mail import send_mail
# from django.core.mail import EmailMessage

from django.conf import settings

# Create your views here.

def rfact(c,r):
    return {i[0]:r[c.description.index(i)] for i in c.description}

    
def signup(request):
    stat=''
    dl=[]
    print(request.method)

    if request.method=='POST':
      print(request.POST)
      un=request.POST['Username']
      m=request.POST['email']
      # pwd=request.POST['password']
      print ("The random id : ",end="")

      string=uuid.uuid4().hex
      password=string[-4:]
      print(password)
      send_mail( f"Hello '{un}' Your registration was succesful", f"new acount password :'{password}'",'krishna1024ray@gmail.com',[m],fail_silently=False)
      # email = EmailMessage('Account verification', f"Hello '{un}' Your registration was succesful", f"new acount password :'{password}'", to=[m])
      # email.send()
    
      dateTimeObj = datetime.now()

      sqlb=f"INSERT INTO rgstr(Username,email,password,datetime) VALUES('{un}','{m}','{password}','{ dateTimeObj}')"
      c=connection.cursor()
      c.execute(sqlb)
      # n=c.lastrowid
      c.close()
      # if n>=0:
      return HttpResponseRedirect('/login/',request)

      # return HttpResponseRedirect('/index/',request)

    return render(request,'signup.html',{'msg':stat,'rgstr':dl})

def login(request):
    print(request)
    stat=""
    if request.method=='POST':
      print(request.method)
      u=request.POST['email']
      p=request.POST['pass']
      c=connection.cursor()
      c.execute(f"SELECT * from rgstr WHERE email ='{u}' and password= '{p}'")
      r=c.fetchone()
      c.close()
      if r:
        request.session['usr']=u
        return HttpResponseRedirect('/card/',request)
      stat="Invalid login...try again"
    t=loader.get_template('login.html')
    return HttpResponse(t.render({'msg':stat},request))


def card(request): 
    stat=''
    c=connection.cursor()
    c.cursor.row_factory=rfact      
    c.execute("select * from subjectlist")
    r=c.fetchall()
    c.close()
    dl=[]
    if r:
        dl=r 

        print (dl)
        return render(request,'card.html',{'msg':stat,'subjectlist':dl})

def subject(request):
    stat=''
    dl=[]
    c=connection.cursor()
    c.cursor.row_factory=rfact
    c.execute("select * from subjectlist")
    r=c.fetchall()
    c.close()
    dl=[]
    if r:
        dl=r
        print (dl)
    print (request.method)
    if request.method=='POST':
      print(request.POST)
      sn=request.POST['subname']
      m=request.POST['marks']
      sql=f"INSERT INTO subjectlist(subjects,maxmarks) VALUES('{sn}','{m}')"
      c=connection.cursor()
      c.execute(sql)
      n=c.lastrowid
      c.close()
      if n>=0:
              return HttpResponseRedirect('/card/',request)

      return HttpResponseRedirect('/subject/',request)

    return render(request,'subject.html',{'msg':stat,'subjectlist':dl})

def delsub(request,subid):
    c=connection.cursor()
    c.execute(f"DELETE FROM subjectlist WHERE subid={subid}")
    c.close()
    print('removed',subid)
    return HttpResponseRedirect('/subject/',request)
    return render(request,'subject.html',{'msg':stat,'subjectlist':dl})

def editsub(request,subjid):
    stat=''
    dl=[]
    print(request.method)
    if request.method=='POST':
      print(request.method)
      sn=request.POST["editsub"]
      ns=request.POST["subnew"]
    c=connection.cursor()
    c.execute(f"UPDATE subjectlist SET subjects='{ns}' WHERE subid='{subjid}'")
    c.close()
    print(' successfully updated',subjid)
    return HttpResponseRedirect('/subject/',request)
  
def index(request):
  
    return render(request,'index.html')   


