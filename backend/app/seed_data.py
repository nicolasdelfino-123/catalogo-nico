"""
Archivo para crear las categorías base del catálogo.
"""

from app import db
from app.category_config import PERFUME_CATEGORY_DEFINITIONS
from app.models import Category


def seed_database():
    """Crear o actualizar las categorías canónicas."""
    for item in PERFUME_CATEGORY_DEFINITIONS:
        category = Category.query.get(item["id"])
        if category:
            category.name = item["name"]
            category.description = item.get("description", "")
            continue

        existing = Category.query.filter_by(name=item["name"]).first()
        if existing:
            existing.description = item.get("description", "")
            continue

        db.session.add(Category(
            id=item["id"],
            name=item["name"],
            description=item.get("description", ""),
        ))

    try:
        db.session.commit()
        print("Categorías creadas/actualizadas correctamente.")
        print(f"Total categorías canónicas: {len(PERFUME_CATEGORY_DEFINITIONS)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear categorías: {e}")


if __name__ == "__main__":
    from app.run import app

    with app.app_context():
        seed_database()
