# AnimeMangaDB Platform v3 Domain Specification

## 1. Purpose

This document is the authoritative domain specification for AnimeMangaDB Platform v3.

It defines what the platform represents, how its core entities relate, which entities own other entities, how identity is determined, and which rules all implementations must preserve.

The domain specification is independent of database technology, ORM implementation, API design, frontend design, provider implementation, and scraper implementation.

Implementation code must conform to this specification.

## 2. Scope

Platform v3 models adaptation relationships between anime episodes and manga chapters within a shared series.

The initial domain includes:

- Series
- Anime Title
- Episode
- Manga Title
- Chapter
- Episode-Chapter Mapping

Additional media types require a future domain decision.

## 3. Domain philosophy

### 3.1 The domain drives the architecture

The platform is designed from the domain model outward. Database convenience, API shape, provider limitations, and frontend presentation must not redefine domain ownership or identity.

### 3.2 Series-first organization

`Series` is the aggregate root. Anime and manga are parallel branches under a series.

```text
Series
├── Anime Titles
│   └── Episodes
│       └── Adapted Chapters
└── Manga Titles
    └── Chapters
        └── Adapted Episodes
```

### 3.3 Explicit adaptation mappings

Episodes and chapters do not own one another. Their relationship is represented by an explicit `EpisodeChapterMapping`.

### 3.4 No recursive ownership

Bidirectional navigation may be offered by services or API responses, but ownership remains acyclic.

## 4. Terminology

### Series

The aggregate root representing a shared franchise, property, or narrative grouping.

### Anime Title

A distinct animated production within a Series.

### Episode

A numbered or otherwise identified installment belonging to exactly one Anime Title.

### Manga Title

A distinct manga publication within a Series.

### Chapter

A numbered or otherwise identified installment belonging to exactly one Manga Title.

### Episode-Chapter Mapping

An explicit adaptation relationship between one Episode and one Chapter.

### Adaptation

A relationship in which anime content is derived from, corresponds to, or otherwise maps to manga source material.

### Canonical title

The preferred title used by AnimeMangaDB for stable display and internal reference.

### Alternate title

A recognized title variant that does not replace the canonical title.

### Slug

A stable, URL-safe lookup and routing identifier.

### Mapping metadata

Information describing the adaptation relationship itself rather than either endpoint.

### Provider

An external source or source-specific integration used to discover or collect data.

### Provenance

Information describing where a value or mapping came from.

### Certified dataset

A dataset that has passed the project's defined validation and certification process for a stated scope version.

## 5. Aggregate root

### 5.1 Series is the aggregate root

Every Anime Title and Manga Title belongs to exactly one Series.

A Series may contain zero or more Anime Titles and zero or more Manga Titles. A publishable Series must contain at least one media title. A draft Series may temporarily contain none during an incomplete import workflow.

### 5.2 Series responsibilities

A Series owns canonical identity, canonical title, slug, alternate titles, Anime Titles, and Manga Titles.

A Series does not own Episode metadata, Chapter metadata, or adaptation mappings directly.

## 6. Entity definitions

## 6.1 Series

### Definition

The root entity grouping all supported anime and manga titles belonging to the same platform-level property.

### Required attributes

- stable identifier
- canonical title
- slug

### Relationships

- owns zero or more Anime Titles
- owns zero or more Manga Titles

### Constraints

- canonical title must not be blank
- slug must not be blank
- slug must be globally unique
- a publishable Series must contain at least one Anime Title or Manga Title

## 6.2 Anime Title

### Definition

A distinct animated production within one Series.

### Required attributes

- stable identifier
- parent Series identifier
- canonical title
- slug
- media classification

### Relationships

- belongs to exactly one Series
- owns zero or more Episodes

### Constraints

- canonical title and slug must not be blank
- slug must be unique within its Series
- an Anime Title cannot belong to multiple Series

The initial media classifications are television, original video animation, original net animation, special, and movie. Movie representation requires an explicit implementation decision and must not be silently forced into an Episode model.

## 6.3 Episode

### Definition

A single installment belonging to one Anime Title.

### Required attributes

- stable identifier
- parent Anime Title identifier
- local episode identity
- display label

### Relationships

- belongs to exactly one Anime Title
- participates in zero or more Episode-Chapter Mappings

### Constraints

- cannot belong to multiple Anime Titles
- local identity must be unique within its Anime Title
- may exist without Chapter mappings
- may adapt Chapters from one or more Manga Titles within the same Series

Local episode identity must support more than positive integers, including values such as `12.5`, `SP1`, and `OVA-2`.

## 6.4 Manga Title

### Definition

A distinct manga publication within one Series.

### Required attributes

- stable identifier
- parent Series identifier
- canonical title
- slug

### Relationships

- belongs to exactly one Series
- owns zero or more Chapters

### Constraints

- canonical title and slug must not be blank
- slug must be unique within its Series
- a Manga Title cannot belong to multiple Series

## 6.5 Chapter

### Definition

A single installment belonging to one Manga Title.

### Required attributes

- stable identifier
- parent Manga Title identifier
- local chapter identity
- display label

### Relationships

- belongs to exactly one Manga Title
- participates in zero or more Episode-Chapter Mappings

### Constraints

- cannot belong to multiple Manga Titles
- local identity must be unique within its Manga Title
- may exist without Episode mappings
- may map to Episodes from multiple Anime Titles within the same Series

Local chapter identity must support more than positive integers, including `0`, `12.5`, `EX`, and `Special-1`.

## 6.6 Episode-Chapter Mapping

### Definition

An explicit relationship connecting one Episode and one Chapter.

### Required attributes

- stable identifier
- Episode identifier
- Chapter identifier

### Optional attributes

- coverage classification
- source start marker
- source end marker
- adaptation order
- confidence
- notes
- provenance metadata
- certification status

### Constraints

- both endpoints must resolve to the same Series
- the Episode-Chapter pair must be unique
- the mapping owns neither endpoint
- deleting a mapping does not delete either endpoint
- deleting an endpoint must not leave an invalid mapping

Cross-Series mappings are forbidden in the initial domain.

## 7. Relationship model

```text
Series 1 ─────── 0..* Anime Title
Series 1 ─────── 0..* Manga Title
Anime Title 1 ── 0..* Episode
Manga Title 1 ── 0..* Chapter
Episode 1 ────── 0..* Episode-Chapter Mapping
Chapter 1 ────── 0..* Episode-Chapter Mapping
```

The tree defines ownership. The mapping defines adaptation.

## 8. Ownership rules

- Series owns Anime Titles and Manga Titles.
- Anime Title owns Episodes.
- Manga Title owns Chapters.
- Episode owns Episode-specific metadata.
- Chapter owns Chapter-specific metadata.
- Episode-Chapter Mapping owns relationship metadata.

Forbidden assumptions:

- Episode owns Chapter
- Chapter owns Episode
- Anime Title owns Manga Title
- Manga Title owns Anime Title
- Episode repository owns Chapter persistence
- Chapter repository owns Episode persistence

Deletion policy must preserve referential validity. Hard-delete, soft-delete, and archival behavior will be specified later.

## 9. Identity rules

Every entity must have a stable identifier independent of display text.

Business uniqueness:

- Series: globally unique Series slug
- Anime Title: Series + Anime Title slug
- Episode: Anime Title + local episode identity
- Manga Title: Series + Manga Title slug
- Chapter: Manga Title + local chapter identity
- Mapping: Episode + Chapter

Duplicate mappings for the same pair are forbidden. Multiple evidence sources belong to one logical mapping rather than duplicate mappings.

## 10. Validation rules

Canonical titles must be strings, nonblank after trimming, and preserve meaningful punctuation.

Slugs must be strings, nonblank, URL-safe, and follow one documented normalization policy.

Parent rules:

- every Anime Title requires a Series
- every Manga Title requires a Series
- every Episode requires an Anime Title
- every Chapter requires a Manga Title
- every mapping requires an Episode and Chapter

Mapping rules:

- both endpoints must exist
- both endpoints must belong to the same Series
- duplicate pairs are forbidden
- optional relationship metadata may be absent
- a mapping never implies ownership

Valid empty relationships include Series with only one media branch, draft titles with no installments, Episodes with no Chapter mappings, and Chapters with no Episode mappings.

The domain must not require all local Episode or Chapter identities to be positive integers.

An Episode may map to Chapters from multiple Manga Titles within its Series. A Chapter may map to Episodes from multiple Anime Titles within its Series.

## 11. Lifecycle rules

### Draft

An entity may be incomplete while being discovered, imported, or edited.

### Validated

An entity has passed structural and domain validation.

### Certified

An entity or dataset scope has passed project certification requirements for a stated scope and dataset version.

### Archived

An entity may be retained but excluded from normal active results.

Content status, publication status, import status, and certification status are separate concerns. One generic status field must not represent all lifecycle dimensions.

## 12. Domain invariants

1. Every Anime Title belongs to exactly one Series.
2. Every Manga Title belongs to exactly one Series.
3. Every Episode belongs to exactly one Anime Title.
4. Every Chapter belongs to exactly one Manga Title.
5. Each EpisodeChapterMapping represents exactly one Episode–Chapter relationship.
    - An Episode may participate in zero or more mappings.
    - A Chapter may participate in zero or more mappings.
    - Together, these mappings allow many-to-many adaptation relationships without introducing recursive ownership.
6. Every mapping connects endpoints from the same Series.
7. Episode and Chapter ownership is never recursive.
8. Duplicate Episode-Chapter pairs are forbidden.
9. Stable identifiers do not change when display titles change.
10. Infrastructure layers do not redefine domain identity.

## 13. Representative examples

### Naruto

```text
Naruto
├── Anime Titles
│   ├── Naruto
│   └── Naruto Shippuden
└── Manga Titles
    └── Naruto
```

A Naruto Chapter may map to Episodes from Naruto, Naruto Shippuden, both, or neither, while remaining within the Naruto Series.

### One Piece

```text
One Piece
├── Anime Titles
│   └── One Piece
└── Manga Titles
    └── One Piece
```

An Episode may map to one Chapter, several Chapters, part of a Chapter, or no Chapter. Relationship-specific details belong to mappings.

### Future remake

```text
Example Series
├── Anime Titles
│   ├── Original Adaptation
│   └── New Adaptation
└── Manga Titles
    └── Original Manga
```

Both adaptations may map independently to the same Chapters without restructuring the domain.

## 14. Future expansion

The architecture must permit later support for remakes, sequels, OVAs, ONAs, specials, movies, multiple manga publications, spin-offs, side stories, anthology chapters, regional numbering, alternate release orders, multilingual titles, volumes, seasons, cours, adaptation coverage, confidence, provenance, novels, web novels, games, and live-action adaptations.

Future media types must not be added by overloading Anime Title or Manga Title with incompatible behavior. A new media branch or generalized media model requires an explicit ADR.

## 15. Out of scope for v0.3.0

This specification does not define SQL tables, ORM relationships, migrations, repositories, REST endpoints, response schemas, frontend routes, provider selectors, crawler scheduling, scraper logic, parser logic, deployment, authentication, or authorization.

## 16. Change control

Any future change to entity ownership, business identity, relationship cardinality, aggregate boundaries, invariants, or media semantics requires:

1. an updated Domain Specification
2. a new or superseding ADR
3. updated validation
4. implementation changes
5. regression tests
6. certification

Implementation code must not introduce new domain behavior before the corresponding specification change is approved.
