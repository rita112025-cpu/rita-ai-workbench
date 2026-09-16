"""Parsing and extraction, the part Scrapling actually does here.

Uses ``scrapling.parser.Selector`` for CSS selection and for adaptive element
relocation: an element matched on a good run is saved to a local SQLite store,
and a later run whose selector no longer matches asks Scrapling to find the same
element again in the changed DOM.

API verified against Scrapling 0.4.15:
``Selector(content=..., url=..., adaptive=..., storage_args={"storage_file": ...})``
and ``Selector.css(selector, adaptive=..., auto_save=..., identifier=...)``
returning a ``Selectors`` sequence with ``.first`` / ``.length``. There is no
``css_first``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from scrapling.parser import Selector

from .errors import CollectorError, ErrorCode
from .models import ExtractionRule


class Document:
    """A parsed page. Wraps Scrapling so no Selector escapes this package."""

    def __init__(
        self,
        html: str,
        *,
        url: str = "",
        adaptive: bool = False,
        storage_file: str | Path | None = None,
    ) -> None:
        self.url = url
        self._adaptive = adaptive
        storage_args: dict[str, Any] | None = None
        if adaptive:
            if storage_file is None:
                raise CollectorError(
                    ErrorCode.EXTRACTION_ERROR,
                    "adaptive extraction needs an explicit storage_file",
                    url=url or None,
                )
            # Keep the element store inside this project's output directory
            # rather than writing into the installed scrapling package.
            Path(storage_file).parent.mkdir(parents=True, exist_ok=True)
            storage_args = {"storage_file": str(storage_file), "url": url}
        try:
            if storage_args is not None:
                self._selector = Selector(
                    content=html, url=url, adaptive=True, storage_args=storage_args
                )
            else:
                self._selector = Selector(content=html, url=url, adaptive=False)
        except Exception as exc:  # noqa: BLE001 - lxml raises a wide variety
            raise CollectorError(
                ErrorCode.EXTRACTION_ERROR, f"could not parse document: {exc}", url=url or None
            ) from exc

    @property
    def adaptive_enabled(self) -> bool:
        return self._adaptive

    def title(self) -> str | None:
        first = self._first("title")
        if first is None:
            return None
        return str(first.text).strip() or None

    def _first(self, selector: str) -> Any | None:
        """``Selectors.first`` is None on an empty match, so never index blindly."""
        found = self._selector.css(selector)
        return found.first if len(found) else None

    def text(self) -> str:
        """Readable body text.

        ``get_all_text()`` already drops script and style content; a
        ``*::text`` selection does not, and would fold CSS and JS source into
        the extracted text.
        """
        node: Any = self._first("body") or self._selector
        return str(node.get_all_text()).strip()

    def select(self, rule: ExtractionRule) -> Any:
        """Apply one rule, honouring adaptive relocation when asked for.

        ``auto_save`` is only meaningful when the Selector was constructed with
        ``adaptive=True``; Scrapling warns and ignores it otherwise, so it is
        passed only in that case.
        """
        kwargs: dict[str, Any] = {}
        if rule.adaptive and self._adaptive:
            kwargs = {"adaptive": True, "auto_save": True, "identifier": rule.name}
        try:
            found = self._selector.css(rule.selector, **kwargs)
        except Exception as exc:  # noqa: BLE001 - invalid selectors raise from cssselect
            raise CollectorError(
                ErrorCode.EXTRACTION_ERROR,
                f"selector {rule.selector!r} is not usable: {exc}",
                url=self.url or None,
            ) from exc

        if not len(found):
            if rule.required:
                raise CollectorError(
                    ErrorCode.EXTRACTION_ERROR,
                    f"required field {rule.name!r} matched nothing for {rule.selector!r}",
                    url=self.url or None,
                )
            return [] if rule.many else None

        values = [_value_of(node, rule.attribute) for node in found]
        return values if rule.many else values[0]

    def save_for_adaptive(self, rule: ExtractionRule) -> bool:
        """Remember the element a rule currently matches, for later relocation.

        Returns False when there is nothing to save, rather than pretending.
        """
        if not self._adaptive:
            return False
        found = self._selector.css(rule.selector)
        if not len(found):
            return False
        # Scrapling 0.4.15: save(element, identifier), called on the document
        # selector with the element to remember -- not element.save(identifier).
        self._selector.save(found.first, rule.name)
        return True

    def extract(self, rules: Sequence[ExtractionRule]) -> dict[str, Any]:
        return {rule.name: self.select(rule) for rule in rules}


def _value_of(node: Any, attribute: str | None) -> str | None:
    if attribute is None:
        text = str(node.text).strip()
        return text or None
    value = node.attrib.get(attribute)
    return str(value).strip() if value is not None else None


def extract_from_html(
    html: str,
    rules: Sequence[ExtractionRule],
    *,
    url: str = "",
    adaptive: bool = False,
    storage_file: str | Path | None = None,
) -> Mapping[str, Any]:
    """Convenience wrapper for callers that only want the fields."""
    return Document(html, url=url, adaptive=adaptive, storage_file=storage_file).extract(rules)
