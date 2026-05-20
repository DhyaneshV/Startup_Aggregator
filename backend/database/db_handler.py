from .models import Opportunity
from mongoengine.errors import NotUniqueError, ValidationError
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpportunityDB:
    @staticmethod
    def add_opportunity(data):
        """Adds a single opportunity to the database with date parsing."""
        try:
            # Handle deadline parsing
            raw_deadline = data.get('deadline')
            if raw_deadline:
                if isinstance(raw_deadline, str):
                    if raw_deadline.lower() in ['rolling', 'rolling applications', 'ongoing']:
                        data['deadline'] = None
                        data['deadline_text'] = raw_deadline
                    else:
                        try:
                            # Try to parse YYYY-MM-DD
                            parsed_date = datetime.strptime(raw_deadline, '%Y-%m-%d')
                            data['deadline'] = parsed_date
                            data['deadline_text'] = parsed_date.strftime('%b %d, %Y')
                        except ValueError:
                            # If parsing fails, store as text and keep date null
                            data['deadline'] = None
                            data['deadline_text'] = raw_deadline
            
            opp = Opportunity(**data)
            opp.save()
            logger.info(f"Successfully added: {opp.title}")
            return True, "Added"
        except NotUniqueError:
            logger.warning(f"Duplicate entry skipped: {data.get('title')}")
            return False, "Duplicate"
        except ValidationError as e:
            logger.error(f"Validation error for {data.get('title')}: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error adding opportunity: {e}")
            return False, str(e)

    @staticmethod
    def get_all_opportunities(filters=None, sort_by='deadline'):
        """Retrieves opportunities with optional filtering and sorting."""
        query = Opportunity.objects
        if filters:
            if 'opportunity_type' in filters and filters['opportunity_type']:
                query = query(opportunity_type=filters['opportunity_type'])
            if 'source' in filters and filters['source']:
                query = query(source=filters['source'])
            if 'region' in filters and filters['region']:
                # Support "India" vs "International" (anything not India)
                if filters['region'].lower() == 'india':
                    query = query(region__icontains='India')
                elif filters['region'].lower() == 'international':
                    query = query(region__not__icontains='India')
                else:
                    query = query(region__icontains=filters['region'])
            if 'keyword' in filters and filters['keyword']:
                query = query.search_text(filters['keyword'])
            
            # Timeline (Deadline) Filtering
            if 'timeline' in filters and filters['timeline']:
                now = datetime.utcnow()
                if filters['timeline'] == 'soon':
                    # Expiring in next 7 days
                    from datetime import timedelta
                    seven_days = now + timedelta(days=7)
                    query = query(deadline__gte=now, deadline__lte=seven_days)
                elif filters['timeline'] == 'upcoming':
                    query = query(deadline__gt=now)
                elif filters['timeline'] == 'rolling':
                    query = query(deadline=None)
        
        if sort_by == 'newest':
            return query.order_by('-created_at')
        elif sort_by == 'deadline':
            # Sort by deadline, nulls (rolling) last
            return query.order_by('deadline')
        else:
            return query.order_by('deadline')

    @staticmethod
    def get_stats():
        """Returns statistics about stored opportunities."""
        return {
            "total_count": Opportunity.objects.count(),
            "types": Opportunity.objects.distinct("opportunity_type"),
            "sources": Opportunity.objects.distinct("source"),
            "regions": Opportunity.objects.distinct("region")
        }
