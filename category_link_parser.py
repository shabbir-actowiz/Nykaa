import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode

from db import PRODUCT_LINK_LIMIT

BASE_URL="https://www.nykaafashion.com"
PRODUCT_LIST_PATH="/rest/appapi/V2/categories/products"

DEFAULT_QUERY_PARAMS={
    "PageSize": str(PRODUCT_LINK_LIMIT),
    "filter_format": "v2",
    "apiVersion": "6",
    "currency": "INR",
    "country_code": "IN",
    "deviceType": "WEBSITE",
    "sort": "popularity",
    "device_os": "desktop",
    "currentPage": "1",
    "sort_algo": "ltr_pinning",
}


def load_json(file_path: str | Path) -> dict[str, Any]:
    with Path(file_path).open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text=str(value).strip()
    if not text:
        return None
    return " ".join(text.split())


def normalize_url(value: Any) -> str | None:
    text=clean_text(value)
    if text is None:
        return None
    if text.startswith("http://") or text.startswith("https://"):
        return text
    if not text.startswith("/"):
        text=f"/{text}"
    return f"{BASE_URL}{text}"


def build_product_list_url(category_id: Any, page: int=1, extra_params: dict[str, Any] | None=None) -> str:
    query_params=DEFAULT_QUERY_PARAMS.copy()
    query_params["currentPage"]=str(page)
    query_params["categoryId"]=str(category_id)

    if extra_params:
        for key, value in extra_params.items():
            if value is not None:
                query_params[key]=str(value)

    return f"{BASE_URL}{PRODUCT_LIST_PATH}?{urlencode(query_params)}"


def parse_filter_data(value: Any) -> dict[str, str]:
    text=clean_text(value)
    if text is None:
        return {}

    parsed_pairs=parse_qsl(text, keep_blank_values=True)
    return {key: val for key, val in parsed_pairs if key}


def _category_has_content(node: dict[str, Any]) -> bool:
    for key in ("id", "name", "action_url", "url", "children_data", "children"):
        value=node.get(key)
        if isinstance(value, list):
            if value:
                return True
        elif value not in (None, "", []):
            return True
    return False


def parse_category_node(
    node: dict[str, Any],
    *,
    parent_id: int | None=None,
    ancestry: list[str] | None=None,
    depth: int=0,
    source_section: str="menu",
) -> dict[str, Any] | None:
    if not isinstance(node, dict) or not _category_has_content(node):
        return None

    category_id=node.get("id")
    category_name=clean_text(node.get("name") or node.get("label") or node.get("title"))
    action_url=normalize_url(node.get("action_url") or node.get("url"))
    sort_value=clean_text(node.get("sort"))
    filter_data=parse_filter_data(node.get("filter_data"))
    level=node.get("level")
    if not isinstance(level, int):
        level=depth

    current_ancestry=list(ancestry or [])
    if category_name:
        current_ancestry.append(category_name)

    children_source=node.get("children_data") or node.get("children") or []
    children: list[dict[str, Any]]=[]
    for child_node in children_source:
        parsed_child=parse_category_node(
            child_node,
            parent_id=category_id if category_id is not None else parent_id,
            ancestry=current_ancestry,
            depth=depth + 1,
            source_section=source_section,
        )
        if parsed_child is not None:
            children.append(parsed_child)

    parsed={
        "source_id": category_id,
        "category_name": category_name or (current_ancestry[-1] if current_ancestry else None),
        "category_path": " > ".join(current_ancestry) if current_ancestry else category_name,
        "category_url": action_url,
        "product_api_url": build_product_list_url(category_id, extra_params={**filter_data, **({"sort": sort_value} if sort_value else {})}) if category_id is not None else None,
        "category_level": level,
        "source_section": source_section,
        "sort": sort_value,
        "filter_data": filter_data,
        "children": children,
    }

    if not category_name and not action_url and not children:
        return None

    return parsed


def extract_category_tree(payload: dict[str, Any]) -> list[dict[str, Any]]:
    menu_items=payload.get("app", {}).get("menu", {}).get("data", [])
    parsed_items: list[dict[str, Any]]=[]

    for item in menu_items:
        parsed_item=parse_category_node(item, source_section="menu")
        if parsed_item is not None:
            parsed_items.append(parsed_item)

    return parsed_items


def flatten_category_tree(tree: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]]=[]

    def walk(node: dict[str, Any]) -> None:
        children=node.get("children", [])
        if not children:
            flattened.append({
                "source_id": node.get("source_id"),
                "category_name": node.get("category_name"),
                "category_path": node.get("category_path"),
                "category_url": node.get("category_url"),
                "product_api_url": node.get("product_api_url")
                # "sort": node.get("sort"),
                # "filter_data": node.get("filter_data"),
            })
            return

        for child in children:
            walk(child)

    for node in tree:
        walk(node)

    return flattened


def parse_category_file(file_path: str | Path) -> dict[str, list[dict[str, Any]]]:
    payload=load_json(file_path)
    tree=extract_category_tree(payload)
    flat=flatten_category_tree(tree)
    return {
        "categories": flat,
    }
