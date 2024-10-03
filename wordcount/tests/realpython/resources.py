from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import getmembers, isclass, isfunction
from typing import Callable


@dataclass(frozen=True)
class Resource(ABC):
    slug: str
    title: str | None = None

    @property
    def slug_clean(self) -> str:
        return self.slug.strip("/")

    @property
    def title_pretty(self) -> str:
        if self.title is None:
            return self.slug_clean.replace("-", " ").title()
        else:
            return self.title

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    def __str__(self) -> str:
        return f"[{self.title_pretty}]({self.url})"


class Tutorial(Resource):
    @property
    def url(self) -> str:
        return f"https://realpython.com/{self.slug_clean}/"


class Course(Resource):
    @property
    def url(self) -> str:
        return f"https://realpython.com/courses/{self.slug_clean}/"


class LearningPath(Resource):
    @property
    def url(self) -> str:
        return f"https://realpython.com/learning-paths/{self.slug_clean}/"


class Podcast(Resource):
    @property
    def url(self) -> str:
        return f"https://realpython.com/podcasts/rpp/{self.slug_clean}/"

    def __str__(self) -> str:
        episode = f"Episode {self.slug_clean}"
        if self.title:
            return f"[{episode}: {self.title_pretty}]({self.url})"
        else:
            return f"[{episode}]({self.url})"


def tutorial(slug: str, title: str | None = None) -> Callable:
    return _associate(Tutorial, slug, title)


def course(slug: str, title: str | None = None) -> Callable:
    return _associate(Course, slug, title)


def learning_path(slug: str, title: str | None = None) -> Callable:
    return _associate(LearningPath, slug, title)


def podcast(slug: str, title: str | None = None) -> Callable:
    return _associate(Podcast, slug, title)


def _associate(
    resource: type, slug: str, title: str | None = None
) -> Callable:
    def decorator(obj: type | Callable) -> type | Callable:
        match obj:
            case cls if isclass(obj):
                for name, function in getmembers(cls, isfunction):
                    if name.startswith("test"):
                        setattr(cls, name, decorator(function))
            case test_function if isfunction(obj):
                if not hasattr(test_function, "resources"):
                    test_function.resources = set()
                test_function.resources.add(resource(slug, title))
        return obj

    return decorator
