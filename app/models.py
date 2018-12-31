from . import db
from  werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin

from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))



class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship("User",backref='role',lazy='dynamic')
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)

    

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMENT|
                         Permission.WRITE_ARTICLES|
                         Permission.MODERATE_COMMENTS,False),
            'Administrator':(0Xff,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=role)
                role.default=roles[r][1]
                role.perssions=roles[r][0]
                db.session.add(role)
            db.session.commit()




class Permission:
    FOLLOW=0X01
    COMMENT=0X02
    WRITE_ARTICLES=0X04
    MODERATE_COMMENTS=0X08
    ADMINISTER=0X80












class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed=db.Column(db.Boolean,default=False)


    def generat_cofirmation_token(self,expiration=2600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def cofirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.dumps(token)
        except:return  False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True
        
        






    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verif_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return '<User %r>'% self.username


