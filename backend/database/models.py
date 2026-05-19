from mongoengine import Document, StringField, DateTimeField, ListField, URLField, DictField
import datetime

class Opportunity(Document):
    meta = {
        'collection': 'opportunities',
        'indexes': [
            'opportunity_type',
            'source',
            'deadline',
            'region',
            '#title',  # Text index for search
            {'fields': ['source_link'], 'unique': True}
        ]
    }
    
    title = StringField(required=True, max_length=200)
    opportunity_type = StringField(required=True) # Removed strict choices
    organizer = StringField(required=True, max_length=200)
    location = StringField(default='Remote')
    region = StringField(default='Global') # For India vs International
    deadline = DateTimeField() # Can be null for rolling
    deadline_text = StringField() # Stores "Rolling Applications" or formatted date
    source_link = URLField(required=True, unique=True)
    apply_link = URLField() # New field for direct application links
    source = StringField(required=True)
    description = StringField()
    eligibility = StringField()
    ai_tags = ListField(StringField(max_length=100))
    timeline = DictField() # Support nested timeline objects as dict
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Opportunity, self).save(*args, **kwargs)
