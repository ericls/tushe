from app import db, bcrypt
from mongoengine import signals
from datetime import datetime


class User(db.Document):
    username = db.StringField(required=True, verbose_name="用户名")
    email = db.StringField(required=True, verbose_name="E-Mail")
    password = db.StringField(verbose_name='修改密码')
    password_hash = db.StringField()
    active = db.BooleanField(default=True, verbose_name="已激活")
    is_admin = db.BooleanField(default=False, verbose_name="管理员")

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.password:
            pw_hash = bcrypt.generate_password_hash(document.password)
            document.password_hash = pw_hash
            document.password = None

    def set_password(self, password):
        pw_hash = bcrypt.generate_password_hash(password)
        self.password_hash = pw_hash
        self.save()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def is_authenticated():
        return True

    def is_active(self):
        return self.active

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username


class Gallery(db.Document):
    gid = db.StringField(primary_key=True, unique=True)
    title = db.StringField()
    user = db.ReferenceField(User)
    pub_date = db.DateTimeField(default=datetime.now)

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        for image in document.images:
            image.gallery.remove(document)
            image.save()

    @property
    def images(self):
        return Image.objects(gallery=self.gid).order_by('-pub-date')

    def __unicode__(self):
        return self.title


class Image(db.Document):
    iid = db.StringField(primary_key=True, unique=True)
    image = db.ImageField(thumbnail_size=(180, 160, True))
    title = db.StringField()
    description = db.StringField()
    user = db.ReferenceField(User)
    pub_date = db.DateTimeField(default=datetime.now)
    view_count = db.IntField(default=0)
    likes = db.IntField(default=0)
    dislikes = db.IntField(default=0)
    tags = db.ListField(db.StringField(max_length=30))
    gallery = db.ListField(db.ReferenceField(Gallery))

    def __unicode__(self):
        return self.title


class Runtime(db.Document):
    wc_access_token = db.StringField(default='')
    wc_access_token_time = db.IntField(default=0)
    rid = db.IntField(default=0, unique=True, primary_key=True)



signals.pre_save.connect(User.pre_save, sender=User)
signals.pre_delete.connect(Gallery.pre_delete, sender=Gallery)
