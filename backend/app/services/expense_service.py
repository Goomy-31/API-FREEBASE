from datetime import datetime
from uuid import uuid4

from backend.app.core.firebase_config import db


def create_expense(user_id, data):
    expense_id = str(uuid4())

    expense = {
        "id": expense_id,
        "amount": data.amount,
        "category": data.category,
        "note": data.note,
        "created_at": datetime.utcnow()
    }

    db.collection("users") \
      .document(user_id) \
      .collection("expenses") \
      .document(expense_id) \
      .set(expense)

    return expense


def get_expenses(user_id):
    docs = db.collection("users") \
             .document(user_id) \
             .collection("expenses") \
             .stream()

    return [doc.to_dict() for doc in docs]