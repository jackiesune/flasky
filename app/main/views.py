from flask import render_template,redirect,session,url_for,current_app

from datetime import datetime

from . import main 
from .. import db
from ..models import User
from ..emails import send_email
from .forms import NameForm

@main.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(name=form.name.data).first()
        if user is None:
            user=User(name=form.name.data)
            db.session.add(user)
            session['known']=False
            db.session.commit()
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('.index'))
    return render_template('index.html',name=session.get('name'),form=form,known=session.get('known',False),current_time=datetime.utcnow())




