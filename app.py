# app.py

from parameter_service import create_app, db
from parameter_service.models.parameter_model import Parameter # Ensure models are imported

app = create_app('development')

# In a development setup, you can create the tables here for convenience
# Note: In production, you'd use a separate migration tool (like Flask-Migrate/Alembic)
with app.app_context():
    db.create_all()

# CRU actions (Future implementation)
# @app.route('/api/v1/parameters', methods=['POST'])
# ...

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)