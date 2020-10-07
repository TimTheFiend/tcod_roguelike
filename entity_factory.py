from components.ai import HostileEnemy
from components import consumable
from components.inventory import Inventory
from components.fighter import Fighter

from entity import Actor, Item


player = Actor(
    char='@',
    color=(255, 255, 255),
    name='Player',
    ai_cls=HostileEnemy,
    fighter=Fighter(
        hp=30,
        defense=2,
        power=5,
    ),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char='☺',
    color=(63, 127, 63),
    name='Orc',
    ai_cls=HostileEnemy,
    fighter=Fighter(
        hp=10,
        defense=0,
        power=3,
    ),
    inventory=Inventory(capacity=0),

)

troll = Actor(
    char='☺',
    color=(48, 138, 135),
    name='Troll',
    ai_cls=HostileEnemy,
    fighter=Fighter(
        hp=16,
        defense=1,
        power=4,
    ),
    inventory=Inventory(capacity=0),

)

health_potion = Item(
    char='¡',
    color=(205, 13, 58),
    name='Health Potion',
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char='Σ',
    color=(188, 209, 50),
    name='Shuriken',
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char='º',
    color=(207, 63, 255),
    name='Confusion Scroll',
    consumable=consumable.ConfusionConsumable(number_of_turns=10)
)
fireball_scroll = Item(
    char='º',
    color=(205, 13, 58),
    name='Fireball Scroll',
    consumable=consumable.FireBallDamageConsumable(damage=12, radius=3)
)