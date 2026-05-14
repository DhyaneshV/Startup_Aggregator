from mongoengine import Document, StringField, DateTimeField, ListField, URLField, DynamicDocument
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
    opportunity_type = StringField(required=True, choices=['Accelerator', 'Grant', 'Conference', 'Job', 'Webinar', 'Other'])
    organizer = StringField(required=True, max_length=100)
    location = StringField(default='Remote')
    region = StringField(default='Global')
    deadline = DateTimeField()
    source_link = URLField(required=True, unique=True)
    source = StringField(required=True)
    description = StringField()
    eligibility = StringField()
    ai_tags = ListField(StringField(max_length=50))
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Opportunity, self).save(*args, **kwargs)
