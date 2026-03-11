import json
from bson import ObjectId, Decimal128
from flask.json.provider import DefaultJSONProvider

class MongoJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Decimal128):
            return float(str(obj)) # Or str(obj) if you need absolute precision
        return super().default(obj)

# # Apply it to your Flask app instance
# app.json = MongoJSONProvider(app)
