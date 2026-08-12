# Let a feature package own its QML enums

Superseded in part by [ADR 0019](0019-dissolve-the-domain-role-into-the-services-role.md): the domain role is
dissolved, and with it the floor this page gave the linter. The enums role, the wire-schema restatement, and
pin-or-translate stand; the plain vocabulary now lives in the services role.

The shared enum package exists to register enums with QML, and two of its members were the import wizard's own
vocabulary. The import domain named one of them, so importing a module of pure rules pulled in seventeen toolkit
modules and ran seven QML registrations as a side effect. The lattice says a domain may import another slice's domain
and nothing else, so the edge sat outside the rule, and the import linter that rule exists to support would have
flagged it on day one.

A feature package owns the QML enums its area means. They get a role directory beside its services, its models and its
view models, and what no feature has claimed stays in the shared enum package, the same way the layer packages hold
every class no feature has claimed. The domain names no QML-registered type. It keeps the plain vocabulary, and the
role directory holds the registration, so a domain stays free of the toolkit and the linter gets a rule it can check:
a domain imports no Qt.

## Why the vocabulary appears twice

The type info generator parses source instead of importing it, and it records only the members a decorated class body
spells out. Handing it an enum built elsewhere registers correctly at runtime and produces type info with no members
at all, so the linter cannot check the names QML uses. The restatement is not duplication that got away from us: it is
the wire schema, and it is the artifact the linter reads.

## Pin or translate

What the domain already says decides which shape the boundary takes.

When the domain names the closed set as an enum, each QML member takes its value from the domain member, and the value
crosses to QML as a plain int with nothing in between. A test pins both the names and the values, because the
generated type info carries names only, so no tool checks the numbers, and a transposition would otherwise render one
page where the domain asked for another.

When the domain names the set as a tagged union, the boundary translates both ways, with a match per direction and
`assert_never` to close it. The type checker then reports a variant or a member added on one side and not the other,
which is a stronger guarantee than the test above and needs no test at all.

Both shapes are in use, and the difference is not an inconsistency to tidy up later. It follows the domain, which
models a wizard step as an enum because the set is closed and flat, and models a session choice as a union because
every other concern is one.

## Consequences

- One area's QML vocabulary reads as one directory, and a slice migrating next moves its enums the way it moves its
  services and its models.
- The domain floor is mechanical: no Qt, no injection. That is one grep, and it states the reason the enum edge was
  wrong rather than only that it was.
- A QML enum is presentation, so a domain never grows a member for a screen that has no domain meaning. A wizard page
  with nothing behind it lives in the enum alone.
- The shared enum package keeps a name that no longer says which enums it holds, since a feature's domain enums are
  enums too. Renaming it is follow-up work.
