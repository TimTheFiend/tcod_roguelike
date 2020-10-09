from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.inventory import Inventory
from components.fighter import Fighter
from components.level import Level

from entity import Actor, Item


player = Actor(
    char='☺',
    color=(255, 255, 255),
    name='Sus',
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(
        hp=30,
        base_def=2,
        base_pow=5,
    ),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char='☻',
    color=(63, 127, 63),
    name='Orc',
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(
        hp=10,
        base_def=0,
        base_pow=3,
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = Actor(
    char='☻',
    color=(48, 138, 135),
    name='Troll',
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(
        hp=16,
        base_def=1,
        base_pow=4,
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

health_potion = Item(
    char='¡',
    color=(205, 13, 58),
    name='Health Potion',
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char='º',
    color=(188, 209, 50),
    name='Lightning Scroll',
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

dagger = Item(
    char='√',
    color=(155, 155, 155),
    name='Dagger',
    equippable=equippable.Dagger()
)

sword = Item(
    char='√',
    color=(192, 192, 192),
    name='Sword',
    equippable=equippable.Sword()
)

leather_armor = Item(
    char='[',
    color=(155,155,155),
    name='Hide armor',
    equippable=equippable.LeatherArmor()
)

chainmail_armor = Item(
    char=']',
    color=(155,155,155),
    name='Chainmail Armor',
    equippable=equippable.ChainMailArmor()
)

