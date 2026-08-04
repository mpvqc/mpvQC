# Group a feature into a feature package

The layer packages sort code by what a class is, not by what it is about. Everything one area means then sits spread
across all of them, held together only by a naming convention. Reading the area means opening every layer and picking
its files out; changing it means touching every layer for one idea. Appearance was spread across four.

An area that has grown that far gets a feature package. Its domain sits at the package root with the types and the pure
rules, and a directory per role it claims holds what it owns: its services, its models, its view models. Tests mirror
the shape. The layer packages keep everything no feature package has claimed, and no re-export shim stays behind, so
call sites name the new home.

Role directories exist because one concept recurs across roles. The same idea is often a domain type, a service and a
model at once, and without the directory each would grow a role suffix to stay distinct. The directory carries the
role, so the concept keeps its name everywhere. The package root exports nothing; each role directory re-exports what
its modules hold, so a call site names the role it pulls from and the layout under that role stays free to change.

A feature package brings its own bindings, and the composition root calls them first. How a service is assembled stops
at the package boundary; the root only decides which packages participate. Bindings must stay lazy, since injection is
configured before `QGuiApplication` exists. QML-facing classes register by decorator when their module is imported, so
startup imports the role directories rather than the bare package, whose empty root would register nothing.

## What stays horizontal

The settings file and the resource bundle stay in the layer packages, and the data files they serve stay where the
bundle wants them. Both are shared boundary services: several areas read through them, and a feature package is one
caller among many. A feature package owns what its area means, not the I/O under it. The file is the seam, not what is
stored in it, so a feature owns the keys it means and reads and writes them through the shared file handle.

## Consequences

- One area is one directory. Reading an area means reading one tree, and the tree names its own dependencies at the
  places it imports across.
- Feature packages and layer packages coexist. Migration of existing leafs is the goal.
- A feature's wiring is reviewable on its own, and adding one touches the root twice: an import and a call.
- Import direction is worth watching. One feature package reaching into another's internals is the failure mode this
  shape makes both easy to write and easy to see.
