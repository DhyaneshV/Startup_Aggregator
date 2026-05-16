from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.database.db_config import DatabaseConfig
from backend.database.db_handler import OpportunityDB
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Enable CORS for frontend integration

# Initialize Database
DatabaseConfig.connect()

@app.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    """Returns a list of startup opportunities with optional filtering."""
    filters = {}
    
    # Extract query parameters
    opp_type = request.args.get('type')
    source = request.args.get('source')
    region = request.args.get('region')
    keyword = request.args.get('q')
    sort_by = request.args.get('sort', 'deadline')

    if opp_type: filters['opportunity_type'] = opp_type
    if source: filters['source'] = source
    if region: filters['region'] = region
    if keyword: filters['keyword'] = keyword

    try:
        opportunities = OpportunityDB.get_all_opportunities(filters, sort_by=sort_by)
        # Convert QuerySet to list of dictionaries
        data = []
        for opp in opportunities:
            data.append({
                "id": str(opp.id),
                "title": opp.title,
                "opportunity_type": opp.opportunity_type,
                "organizer": opp.organizer,
                "location": opp.location,
                "region": opp.region,
                "deadline": opp.deadline.strftime('%Y-%m-%d') if opp.deadline else None,
                "source_link": opp.source_link,
                "source": opp.source,
                "description": opp.description,
                "eligibility": opp.eligibility,
                "ai_tags": opp.ai_tags,
                "created_at": opp.created_at.isoformat() if opp.created_at else None
            })
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching opportunities: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Returns basic stats about the opportunities."""
    try:
        stats = OpportunityDB.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({"error": "Failed to fetch stats"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
