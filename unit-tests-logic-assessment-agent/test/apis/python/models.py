"""Data types for the to-do API."""

from dataclasses import dataclass


@dataclass
class TodoItem:
    """A single to-do item. Priority runs from 1 (lowest) to 5 (highest)."""

    id: int
    title: str
    priority: int
    completed: bool = False
