from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """Represents an example prompt with associated token counts."""

    name: str
    output_tokens: int
    input_tokens: int
    cached_tokens: int

    @property
    def label(self) -> str:
        return f"{self.name} ({self.output_tokens} output tokens)"
