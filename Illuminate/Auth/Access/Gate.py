from typing import Any, Callable, List
from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Helpers.Util import Util


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

    def check(self, abilities: list, arguments: List[Any] = []) -> bool:
        return collect(abilities).every(
            lambda ability: self.inspect(ability, arguments)
        )

    def authorize(self, ability: str, arguments: List[Any] = []):
        assert isinstance(ability, str)

        allowed = self.inspect(ability, arguments)

        if not allowed:
            raise UnauthorizedAccessException("Unauthorized")

    def inspect(self, ability: str | list, arguments: List[Any] = []) -> bool:
        results = self.raw(ability, arguments)

        return results

    def raw(self, ability: str, arguments: List[Any] = []) -> bool:
        arguments = arguments if isinstance(arguments, list) else [arguments]

        user = self.resolve_user()

        auth_callback = self.get_auth_callback(ability, arguments)

        if not auth_callback:
            return True

        return Util.callback_with_dynamic_args(auth_callback, [user, *arguments])

    def get_auth_callback(self, ability: str | list, arguments: List[Any] = []):
        auth_callback = None

        if len(arguments):
            policy_class = self.get_policy_for(arguments[0])

            if policy_class and hasattr(policy_class, ability):
                auth_callback = getattr(policy_class(), ability)

        if not auth_callback:
            ability_callback = self.abilities.get(ability)

            if ability_callback:
                auth_callback = ability_callback

        return auth_callback

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
        if isinstance(
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

    def resolve_user(self):
        return self.user_resolver()

    def resolve_policy(self, policy):
        return self.__app.make(policy)

    def allows(self, ability: str, arguments: List[Any]) -> bool:
        return self.check(ability, arguments)

    def denies(self, ability: str, arguments: List[Any]) -> bool:
        return not self.allows(ability, arguments)
