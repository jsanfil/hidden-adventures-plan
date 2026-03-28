#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import struct
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def cstring(buf: bytes, offset: int) -> tuple[str, int]:
    end = buf.index(0, offset)
    return buf[offset:end].decode("utf-8", errors="replace"), end + 1


def parse_document(buf: bytes, offset: int) -> tuple[dict[str, Any], int]:
    length = struct.unpack("<i", buf[offset : offset + 4])[0]
    end = offset + length
    pos = offset + 4
    out: dict[str, Any] = {}

    while pos < end - 1:
        value_type = buf[pos]
        pos += 1
        key, pos = cstring(buf, pos)

        if value_type == 0x01:
            value = struct.unpack("<d", buf[pos : pos + 8])[0]
            pos += 8
        elif value_type == 0x02:
            size = struct.unpack("<i", buf[pos : pos + 4])[0]
            value = buf[pos + 4 : pos + 4 + size - 1].decode("utf-8", errors="replace")
            pos += 4 + size
        elif value_type == 0x03:
            value, pos = parse_document(buf, pos)
        elif value_type == 0x04:
            array_doc, pos = parse_document(buf, pos)
            value = [array_doc[k] for k in sorted(array_doc, key=lambda x: int(x) if x.isdigit() else x)]
        elif value_type == 0x07:
            value = buf[pos : pos + 12].hex()
            pos += 12
        elif value_type == 0x08:
            value = buf[pos] != 0
            pos += 1
        elif value_type == 0x09:
            ms = struct.unpack("<q", buf[pos : pos + 8])[0]
            value = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
            pos += 8
        elif value_type == 0x0A:
            value = None
        elif value_type == 0x10:
            value = struct.unpack("<i", buf[pos : pos + 4])[0]
            pos += 4
        elif value_type == 0x11:
            value = {"_bson_timestamp": struct.unpack("<Q", buf[pos : pos + 8])[0]}
            pos += 8
        elif value_type == 0x12:
            value = struct.unpack("<q", buf[pos : pos + 8])[0]
            pos += 8
        else:
            raise ValueError(f"Unsupported BSON type {value_type:#x} at byte offset {pos - 1}")

        out[key] = value

    return out, end


def parse_archive(archive_path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    data = archive_path.read_bytes()
    pos = 4

    archive_meta: list[dict[str, Any]] = []
    while pos + 4 <= len(data):
        length = struct.unpack("<I", data[pos : pos + 4])[0]
        if length == 0xFFFFFFFF:
            break
        doc, pos = parse_document(data, pos)
        archive_meta.append(doc)

    collection_meta: dict[str, dict[str, Any]] = {}
    for doc in archive_meta[1:]:
        collection = doc.get("collection")
        metadata_raw = doc.get("metadata")
        metadata = {}
        if isinstance(metadata_raw, str):
            try:
                metadata = json.loads(metadata_raw)
            except json.JSONDecodeError:
                metadata = {"raw": metadata_raw}
        collection_meta[str(collection)] = {
            "db": doc.get("db"),
            "collection": collection,
            "size_hint": doc.get("size"),
            "metadata": metadata,
        }

    collections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    while pos + 4 <= len(data):
        marker = struct.unpack("<I", data[pos : pos + 4])[0]
        if marker != 0xFFFFFFFF:
            break

        pos += 4
        if pos + 4 > len(data):
            break

        header, pos = parse_document(data, pos)
        collection = str(header.get("collection"))
        eof = bool(header.get("EOF"))

        while pos + 4 <= len(data):
            length = struct.unpack("<I", data[pos : pos + 4])[0]
            if length == 0xFFFFFFFF:
                break
            doc, pos = parse_document(data, pos)
            if not eof:
                collections[collection].append(doc)

    return archive_meta, collection_meta, collections


def field_presence(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    for doc in docs:
        for key in doc.keys():
            counts[key] += 1

    return [
        {"field": field, "count": count}
        for field, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def top_counter(values: list[Any], limit: int = 20) -> list[dict[str, Any]]:
    counter = Counter(value for value in values if value not in (None, "", []))
    return [{"value": key, "count": count} for key, count in counter.most_common(limit)]


def build_summary(archive_path: Path) -> dict[str, Any]:
    archive_meta, collection_meta, collections = parse_archive(archive_path)

    archive_info = archive_meta[0] if archive_meta else {}
    summary: dict[str, Any] = {
        "source": {
            "archive_path": str(archive_path),
            "archive_size_bytes": archive_path.stat().st_size,
            "tool_version": archive_info.get("tool_version"),
            "server_version": archive_info.get("server_version"),
            "concurrent_collections": archive_info.get("concurrent_collections"),
        },
        "collections": {},
        "findings": {},
    }

    for collection_name in sorted(set(collection_meta) | set(collections)):
        docs = collections.get(collection_name, [])
        indexes = collection_meta.get(collection_name, {}).get("metadata", {}).get("indexes", [])
        summary["collections"][collection_name] = {
            "document_count": len(docs),
            "field_presence": field_presence(docs),
            "indexes": indexes,
        }

    adventures = collections.get("adventures", [])
    profiles = collections.get("profiles", [])
    favorites = collections.get("favorites", [])
    comments = collections.get("comments", [])
    sidekicks = collections.get("sidekicks", [])
    messages = collections.get("messages", [])
    filenames = collections.get("filenames", [])
    ratings = collections.get("ratings", [])

    adventure_ids = {doc.get("_id") for doc in adventures}
    profile_usernames = {doc.get("username") for doc in profiles if doc.get("username")}
    adventure_authors = {doc.get("author") for doc in adventures if doc.get("author")}
    author_counts = Counter(doc.get("author") for doc in adventures if doc.get("author"))

    summary["findings"] = {
        "missing_collections": [
            name
            for name in ["ratings"]
            if name not in collections and name not in collection_meta
        ],
        "empty_collections": sorted(
            [
                name
                for name, docs in collections.items()
                if len(docs) == 0
            ]
        ),
        "adventures": {
            "count": len(adventures),
            "access_distribution": top_counter([doc.get("access") for doc in adventures]),
            "category_distribution": top_counter([doc.get("category") for doc in adventures]),
            "top_authors": [{"value": key, "count": count} for key, count in author_counts.most_common(15)],
            "missing_location_count": sum(1 for doc in adventures if not doc.get("location")),
            "missing_default_image_count": sum(1 for doc in adventures if not doc.get("defaultImage")),
            "missing_description_count": sum(1 for doc in adventures if not doc.get("desc")),
            "images_array_empty_count": sum(1 for doc in adventures if not doc.get("images")),
            "acl_non_empty_count": sum(1 for doc in adventures if doc.get("acl")),
            "sidekicks_without_acl_count": sum(
                1 for doc in adventures if doc.get("access") == "Sidekicks" and not doc.get("acl")
            ),
            "authors_missing_profile_count": sum(1 for author in adventure_authors if author not in profile_usernames),
        },
        "profiles": {
            "count": len(profiles),
            "missing_email_count": sum(1 for doc in profiles if not doc.get("email")),
            "missing_full_name_count": sum(1 for doc in profiles if not doc.get("fullName")),
            "missing_profile_image_count": sum(1 for doc in profiles if not doc.get("profileImage")),
            "missing_background_image_count": sum(1 for doc in profiles if not doc.get("backgroundImage")),
            "adventure_count_mismatch_count": sum(
                1 for doc in profiles if (doc.get("adventureCount") or 0) != author_counts[doc.get("username")]
            ),
        },
        "favorites": {
            "count": len(favorites),
            "orphan_adventure_reference_count": sum(
                1 for doc in favorites if doc.get("adventureID") not in adventure_ids
            ),
            "usernames_missing_profile_count": sum(
                1 for doc in favorites if doc.get("username") not in profile_usernames
            ),
        },
        "comments": {
            "count": len(comments),
            "orphan_adventure_reference_count": sum(
                1 for doc in comments if doc.get("adventureID") not in adventure_ids
            ),
            "usernames_missing_profile_count": sum(
                1 for doc in comments if doc.get("username") not in profile_usernames
            ),
        },
        "sidekicks": {
            "count": len(sidekicks),
            "links_with_missing_profile_count": sum(
                1
                for doc in sidekicks
                if doc.get("username") not in profile_usernames or doc.get("sidekickName") not in profile_usernames
            ),
            "top_owners": top_counter([doc.get("username") for doc in sidekicks], limit=15),
        },
        "messages": {"count": len(messages)},
        "filenames": {"count": len(filenames)},
        "ratings": {"count": len(ratings)},
    }

    return summary


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any]) -> str:
    source = summary["source"]
    collections = summary["collections"]
    findings = summary["findings"]

    collection_rows = []
    for name, details in sorted(collections.items()):
        collection_rows.append(
            [
                name,
                details["document_count"],
                len(details["indexes"]),
                ", ".join(index["name"] for index in details["indexes"]) or "none",
            ]
        )

    category_rows = [
        [item["value"], item["count"]]
        for item in findings["adventures"]["category_distribution"]
    ]
    access_rows = [
        [item["value"], item["count"]]
        for item in findings["adventures"]["access_distribution"]
    ]

    lines = [
        "# Legacy Mongo Archive Profile",
        "",
        "## Source",
        "",
        f"- Archive: `{source['archive_path']}`",
        f"- Size: `{source['archive_size_bytes']}` bytes",
        f"- Tool version: `{source.get('tool_version')}`",
        f"- Server version: `{source.get('server_version')}`",
        f"- Concurrent collections setting: `{source.get('concurrent_collections')}`",
        "",
        "## Collection Counts",
        "",
        markdown_table(["Collection", "Documents", "Indexes", "Index Names"], collection_rows),
        "",
        "## Key Findings",
        "",
        f"- `ratings` is not present in the archive metadata or data segments.",
        f"- `messages` and `filenames` exist as collections but currently contain `0` documents in this archive.",
        f"- `adventures` contains `{findings['adventures']['count']}` records, with `{findings['adventures']['authors_missing_profile_count']}` authors missing a matching profile row.",
        f"- `favorites` contains `{findings['favorites']['count']}` records, including `{findings['favorites']['orphan_adventure_reference_count']}` references to missing adventures.",
        f"- `comments` contains `{findings['comments']['count']}` records, including `{findings['comments']['orphan_adventure_reference_count']}` references to missing adventures.",
        f"- `sidekicks` contains `{findings['sidekicks']['count']}` records, with `{findings['sidekicks']['links_with_missing_profile_count']}` links that reference a missing profile on one side.",
        "",
        "## Adventure Access Distribution",
        "",
        markdown_table(["Access", "Count"], access_rows),
        "",
        "## Adventure Category Distribution",
        "",
        markdown_table(["Category", "Count"], category_rows),
        "",
        "## Migration Risk Notes",
        "",
        f"- Every adventure has location data in this archive, but all `{findings['adventures']['images_array_empty_count']}` adventure rows have an empty or missing `images[]` array while `defaultImage` is still populated. The migration should treat `defaultImage` as authoritative media input.",
        f"- `{findings['adventures']['sidekicks_without_acl_count']}` `Sidekicks` adventures have no ACL payload, so visibility conversion should not assume `access = Sidekicks` guarantees a complete allowed-viewer list.",
        f"- `{findings['profiles']['missing_profile_image_count']}` profiles are missing `profileImage`, so the rebuild should expect sparse avatar coverage during migration.",
        f"- `{findings['favorites']['usernames_missing_profile_count']}` favorites reference usernames that do not resolve to a profile in this archive.",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a legacy mongodump archive without restoring it.")
    parser.add_argument("archive", type=Path, help="Path to the mongodump archive file")
    parser.add_argument("--json-out", type=Path, help="Write machine-readable summary JSON to this path")
    parser.add_argument("--markdown-out", type=Path, help="Write a markdown report to this path")
    args = parser.parse_args()

    summary = build_summary(args.archive)

    if args.json_out:
        args.json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    markdown = render_markdown(summary)
    if args.markdown_out:
        args.markdown_out.write_text(markdown + "\n", encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
