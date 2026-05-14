import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

class OpportunityDatabase:
    def __init__(self):
        # Using the provided MongoDB URI directly as requested
        self.uri = "mongodb+srv://dhyanesh:Tn-11ah8563@sacluster.tychmo5.mongodb.net/startupAggregator?retryWrites=true&w=majority&appName=SAcluster"
        self.client = MongoClient(self.uri)
        self.db = self.client.startupAggregator
        self.collection = self.db.opportunities
        
        # Ensure a unique index on 'link' to prevent duplicate entries
        self.collection.create_index([("link", ASCENDING)], unique=True)
        # Also create indexes for filtering
        self.collection.create_index([("type", ASCENDING)])
        self.collection.create_index([("source", ASCENDING)])
        self.collection.create_index([("deadline", ASCENDING)])

    def insert_opportunity(self, data):
        """
        Inserts a single opportunity. 
        Uses update_one with upsert=True to handle deduplication based on link.
        """
        try:
            # Check if it already exists by link
            self.collection.update_one(
                {"link": data['link']},
                {"$set": data},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False

    def insert_many(self, opportunities):
        """Inserts multiple opportunities."""
        count = 0
        for opp in opportunities:
            if self.insert_opportunity(opp):
                count += 1
        return count

    def get_opportunities(self, filters=None):
        """Retrieves opportunities based on provided filters."""
        query = {}
        if filters:
            if 'keyword' in filters and filters['keyword']:
                query['$or'] = [
                    {'title': {'$regex': filters['keyword'], '$options': 'i'}},
                    {'organizer': {'$regex': filters['keyword'], '$options': 'i'}},
                    {'location': {'$regex': filters['keyword'], '$options': 'i'}}
                ]
            if 'type' in filters and filters['type']:
                query['type'] = filters['type']
            if 'source' in filters and filters['source']:
                query['source'] = filters['source']
            if 'region' in filters and filters['region']:
                query['location'] = {'$regex': filters['region'], '$options': 'i'}
            
            # Deadline filter (simplified for now, can be expanded to date ranges)
            if 'deadline_start' in filters and 'deadline_end' in filters:
                 query['deadline'] = {
                     '$gte': filters['deadline_start'],
                     '$lte': filters['deadline_end']
                 }

        return list(self.collection.find(query).sort("deadline", ASCENDING))

    def get_stats(self):
        """Returns basic statistics about the collection."""
        return {
            "total_count": self.collection.count_documents({}),
            "types": self.collection.distinct("type"),
            "sources": self.collection.distinct("source")
        }

if __name__ == "__main__":
    # Quick test connection
    db = OpportunityDatabase()
    print("Database connected successfully.")
    print(f"Current Stats: {db.get_stats()}")
