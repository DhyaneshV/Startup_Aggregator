from .models import Opportunity
from mongoengine.errors import NotUniqueError, ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpportunityDB:
    @staticmethod
    def add_opportunity(data):
        """Adds a single opportunity to the database."""
        try:
            # Handle potential date strings if necessary, though DateTimeField expects datetime objects
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
            if 'opportunity_type' in filters:
                query = query(opportunity_type=filters['opportunity_type'])
            if 'source' in filters:
                query = query(source=filters['source'])
            if 'region' in filters:
                query = query(region__icontains=filters['region'])
            if 'keyword' in filters:
                query = query.search_text(filters['keyword'])
        
        if sort_by == 'newest':
            return query.order_by('-created_at')
        else:
            # Default to deadline ascending
            return query.order_by('deadline')

    @staticmethod
    def get_stats():
        """Returns statistics about stored opportunities."""
        return {
            "total_count": Opportunity.objects.count(),
            "types": Opportunity.objects.distinct("opportunity_type"),
            "sources": Opportunity.objects.distinct("source")
        }
