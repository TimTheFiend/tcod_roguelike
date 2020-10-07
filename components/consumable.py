from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.ai
import components.inventory
from components.base_components import BaseComponent
from exceptions import Impossible
from input_handlers import (
    ActionOrHandler,
    AreaRangedAttackHandler,
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.
        `action` is the context for this activation
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amounts_recovered = consumer.fighter.heal(self.amount)

        if amounts_recovered > 0:
            self.engine.message_log.add_message(
                f'You consume the {self.parent.name}, and recover {amounts_recovered} HP.',
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible('Your health is full, homie.')


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.max_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.max_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f'You zap {target.name}, and for a brief second you see the skeleton inside, for {self.damage}',
                color.player_atk,
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible('No one is within range, unless you wanna taze yourself.')


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        self.engine.message_log.add_message(
            'Select a target location.',
            color.needs_target,
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )


    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible('You cannot target what you cannot see.')
        if not target:
            raise Impossible('You must select a target, dummy.')
        if target is consumer:
            raise Impossible('Don\'t be that guy.')

        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireBallDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        self.engine.message_log.add_message(
            'Select a target location',
            color.needs_target,
        )
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )


    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy
        if not self.engine.game_map.visible[target_xy]:
            raise Impossible('You cannot target an area you cannot see.')

        targets_hit = False
        for action in self.engine.game_map.actors:
            if action.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f'The {action.name.lower()} is caught in the fireball, and takes {self.damage} DMG.',
                )
                action.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible('There are no targets in that area')
        self.consume()