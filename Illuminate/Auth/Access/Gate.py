from typing import Any, Callable, List
from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract
from Illuminate.Database.Collection import Collection


class Gate(GateContract):
    def __init__(
        self,
        app,
        user_resolver=lambda: None,
        abilities={},
        policies={},
        before_callbacks: List[Callable[[Any], Any]] = [],
        after_callbacks: List[Callable[[Any], Any]] = [],
    ) -> None:
        self.__app = app
        self.user_resolver = user_resolver
        self.abilities = abilities
        self.policies = policies
        self.before_callbacks = before_callbacks
        self.after_callbacks = after_callbacks

    def before(self, callback: Callable[[Any], Any]):
        if callable(callback):
            self.before_callbacks.append(callback)

        return self

    def after(self, callback: Callable[[Any], Any]):
        if callable(callback):
            self.after_callbacks.append(callback)

        return self

    def define(self, ability: str, callback: Callable[[Any], Any]):
        if callable(callback):
            self.abilities[ability] = callback

    def check(self, ability: str, arguments: List[Any] = []) -> bool:
        abilities = [ability] if isinstance(ability, str) else ability

        return Collection(abilities).every(
            lambda ability: self.inspect(ability, arguments)
        )

    def inspect(self, ability: str, arguments: List[Any] = []) -> bool:
        abilities = [ability] if isinstance(ability, str) else ability

        return all(
            self.abilities.get(ability, lambda *args: False)(*arguments)
            for ability in abilities
        )

    def has(self, abilities: List[str]) -> bool:
        return all(self.abilities.get(ability, None) for ability in abilities)

    def get_policy_for(self, instance_or_class):
        model_class = self.__get_model_class(instance_or_class)

        try:
            return self.policies[model_class]
        except KeyError:
            return None

    def policy(self, instance_or_class, policy):
        model_class = self.__get_model_class(instance_or_class)

        if model_class:
            self.policies[model_class] = policy

    def __get_model_class(self, instance_or_class):
        if not isinstance(
            instance_or_class, (str, bool, int, float, list, dict, tuple, set)
        ):
            return None
        elif isinstance(instance_or_class, type):
            return instance_or_class
        else:
            return instance_or_class.__class__

    def for_user(self, user):
        return Gate(
            app=self.__app,
            user_resolver=lambda: user,
            abilities=self.abilities,
            policies=self.policies,
            before_callbacks=self.before_callbacks,
            after_callbacks=self.after_callbacks,
        )

    def authorize(self, ability, resource):
        return True

    def resolve_user(self):
        return self.user_resolver()

    def resolve_policy(self, policy):
        return self.__app.make(policy)

    def allows(self, ability: str, arguments: List[Any]) -> bool:
        return self.check(ability, arguments)

    def denies(self, ability: str, arguments: List[Any]) -> bool:
        return not self.allows(ability, arguments)
