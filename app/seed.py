import asyncio
from sqlalchemy import select, text

from app.db.db import async_session, engine
from app.models import Building, Organization, OrganizationPhone
from app.models.activity import ActivityType

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/hh"


async def seed_data():
    try:
        async with async_session() as db:
            await db.execute(text("""
                TRUNCATE TABLE 
                    organization_phones,
                    organization_activity,
                    organizations, 
                    buildings, 
                    activity_types 
                RESTART IDENTITY CASCADE
            """))
            await db.commit()

            level1_food = ActivityType(name="Продукты питания", level=1)
            level1_clothes = ActivityType(name="Одежда", level=1)
            level1_services = ActivityType(name="Услуги", level=1)

            level2_dairy = ActivityType(name="Молочная продукция", level=2, parent=level1_food)
            level2_bakery = ActivityType(name="Хлебобулочные изделия", level=2, parent=level1_food)
            level2_meat = ActivityType(name="Мясные продукты", level=2, parent=level1_food)

            level2_shoes = ActivityType(name="Обувь", level=2, parent=level1_clothes)
            level2_clothing = ActivityType(name="Одежда", level=2, parent=level1_clothes)

            level3_cheese = ActivityType(name="Сыры", level=3, parent=level2_dairy)
            level3_milk = ActivityType(name="Молоко", level=3, parent=level2_dairy)
            level3_yogurt = ActivityType(name="Йогурты", level=3, parent=level2_dairy)

            db.add_all([
                level1_food, level1_clothes, level1_services,
                level2_dairy, level2_bakery, level2_meat,
                level2_shoes, level2_clothing,
                level3_cheese, level3_milk, level3_yogurt
            ])
            await db.commit()

            buildings = [
                Building(
                    address="г. Москва, ул. Тверская, д.10",
                    latitude=55.7649,
                    longitude=37.6055
                ),
                Building(
                    address="г. Москва, ул. Арбат, д.25",
                    latitude=55.7497,
                    longitude=37.5906
                ),
                Building(
                    address="г. Москва, пр. Мира, д.101",
                    latitude=55.7942,
                    longitude=37.6319
                )
            ]
            db.add_all(buildings)
            await db.commit()

            activities = {a.name: a for a in (await db.execute(select(ActivityType))).scalars().all()}
            buildings = (await db.execute(select(Building))).scalars().all()

            organizations = [
                Organization(
                    name="Молочные реки",
                    building_id=buildings[0].id,
                    activities=[
                        activities["Молочная продукция"],
                        activities["Сыры"]
                    ],
                    phones=[
                        OrganizationPhone(phone="+7 (495) 111-11-11"),
                        OrganizationPhone(phone="+7 (495) 111-11-12")
                    ]
                ),
                Organization(
                    name="Хлебная лавка",
                    building_id=buildings[0].id,
                    activities=[activities["Хлебобулочные изделия"]],
                    phones=[OrganizationPhone(phone="+7 (495) 222-22-22")]
                ),
                Organization(
                    name="Мясной ряд",
                    building_id=buildings[1].id,
                    activities=[activities["Мясные продукты"]],
                    phones=[OrganizationPhone(phone="+7 (495) 333-33-33")]
                ),
                Organization(
                    name="Обувной бутик",
                    building_id=buildings[2].id,
                    activities=[
                        activities["Обувь"],
                        activities["Одежда"]
                    ],
                    phones=[
                        OrganizationPhone(phone="+7 (495) 444-44-44"),
                        OrganizationPhone(phone="+7 (495) 444-44-45")
                    ]
                )
            ]

            db.add_all(organizations)
            await db.commit()

            print("✅ Тестовые данные успешно созданы!")
            print(
                f"Создано: {len(activities)} видов деятельности, {len(buildings)} зданий, {len(organizations)} организаций")

    except Exception as e:
        print(f"❌ Ошибка при заполнении базы данных: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed_data())