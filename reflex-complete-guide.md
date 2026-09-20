# Reflex (Python) — The Complete End-to-End Guide

> **Pure-Python full-stack web apps: frontend + backend + database, no JavaScript required.**
>
> Written against **Reflex 0.9.x** (latest release checked: **0.9.11, 11 Sep 2026**). Reflex moves fast, so if something in a snippet errors on your machine, run `reflex --version` and compare with the [official changelog](https://reflex.dev/docs/changelog/).

**How to use this guide**

- Use the **Table of Contents** below — every entry is a clickable link. Each section ends with a **↑ Back to top** link.
- Sections named **"Quick reference"** hold tables (arguments, methods, one-line uses). The second index right under the TOC lists them all.
- Every code snippet is followed by a **"How it works"** explanation in plain language.
- All snippets assume this import at the top:

```python
import reflex as rx
```

## Table of Contents

- **[1. Introduction and How Reflex Works](#1-introduction-and-how-reflex-works)**
  - [1.1 What is Reflex?](#11-what-is-reflex)
  - [1.2 Architecture in one picture](#12-architecture-in-one-picture)
  - [1.3 The three core ideas](#13-the-three-core-ideas)
  - [1.4 What is new in 0.9.x (things that may bite old tutorials)](#14-what-is-new-in-09x-things-that-may-bite-old-tutorials)
- **[2. Installation and Project Setup](#2-installation-and-project-setup)**
  - [2.1 Requirements](#21-requirements)
  - [2.2 Create a project](#22-create-a-project)
  - [2.3 Project structure](#23-project-structure)
  - [2.4 The two rules Reflex enforces](#24-the-two-rules-reflex-enforces)
- **[3. CLI Quick Reference](#3-cli-quick-reference)**
- **[4. Your First App](#4-your-first-app)**
  - [4.1 A counter (the "hello world" of Reflex)](#41-a-counter-the-hello-world-of-reflex)
- **[5. The App Object and Pages](#5-the-app-object-and-pages)**
  - [5.1 `rx.App`](#51-rxapp)
  - [5.2 Adding pages](#52-adding-pages)
  - [5.3 The `@rx.page` decorator (same thing, less boilerplate)](#53-the-rxpage-decorator-same-thing-less-boilerplate)
  - [5.4 A custom 404 page](#54-a-custom-404-page)
  - [5.5 A shared page template](#55-a-shared-page-template)
- **[6. Components](#6-components)**
  - [6.1 Anatomy of a component](#61-anatomy-of-a-component)
  - [6.2 Layout components](#62-layout-components)
  - [6.3 Text and typography](#63-text-and-typography)
  - [6.4 Buttons, icons, images, feedback](#64-buttons-icons-images-feedback)
  - [6.5 Overlays and navigation widgets](#65-overlays-and-navigation-widgets)
  - [6.6 Raw HTML elements with `rx.el`](#66-raw-html-elements-with-rxel)
- **[7. Styling and Theming](#7-styling-and-theming)**
  - [7.1 Style props (CSS as keyword arguments)](#71-style-props-css-as-keyword-arguments)
  - [7.2 Responsive design](#72-responsive-design)
  - [7.3 Global and per-component-type styles](#73-global-and-per-component-type-styles)
  - [7.4 Themes (`rx.theme`)](#74-themes-rxtheme)
  - [7.5 Colors](#75-colors)
  - [7.6 Dark / light mode](#76-dark--light-mode)
  - [7.7 Tailwind CSS (optional)](#77-tailwind-css-optional)
- **[8. State and Vars](#8-state-and-vars)**
  - [8.1 Defining state](#81-defining-state)
  - [8.2 Backend-only vars (private)](#82-backend-only-vars-private)
  - [8.3 Computed vars (`@rx.var`)](#83-computed-vars-rxvar)
  - [8.4 Var operations cheat sheet](#84-var-operations-cheat-sheet)
  - [8.5 Mutable vars (lists, dicts, sets)](#85-mutable-vars-lists-dicts-sets)
  - [8.6 Custom types with dataclasses](#86-custom-types-with-dataclasses)
  - [8.7 Substates and inheritance](#87-substates-and-inheritance)
  - [8.8 Resetting and misc state helpers](#88-resetting-and-misc-state-helpers)
  - [8.9 Setters — write them explicitly](#89-setters--write-them-explicitly)
- **[9. Events and Event Handlers](#9-events-and-event-handlers)**
  - [9.1 What is an event handler?](#91-what-is-an-event-handler)
  - [9.2 Passing arguments](#92-passing-arguments)
  - [9.3 Event triggers (props you attach handlers to)](#93-event-triggers-props-you-attach-handlers-to)
  - [9.4 Streaming updates with `yield`](#94-streaming-updates-with-yield)
  - [9.5 Chaining events](#95-chaining-events)
  - [9.6 Event actions (modifiers)](#96-event-actions-modifiers)
  - [9.7 Special events (quick reference)](#97-special-events-quick-reference)
  - [9.8 Background tasks (long-running work)](#98-background-tasks-long-running-work)
  - [9.9 Page load and mount events](#99-page-load-and-mount-events)
- **[10. Conditional Rendering and Loops](#10-conditional-rendering-and-loops)**
  - [10.1 `rx.cond` (if / else)](#101-rxcond-if--else)
  - [10.2 `rx.match` (switch / case)](#102-rxmatch-switch--case)
  - [10.3 Loops with `rx.foreach`](#103-loops-with-rxforeach)
- **[11. Forms and Inputs](#11-forms-and-inputs)**
  - [11.1 A complete form with `on_submit`](#111-a-complete-form-with-on_submit)
  - [11.2 Controlled inputs (live-bound to state)](#112-controlled-inputs-live-bound-to-state)
  - [11.3 Other controls in one example](#113-other-controls-in-one-example)
  - [11.4 Validation pattern](#114-validation-pattern)
  - [11.5 Clearing an input with `rx.set_value`](#115-clearing-an-input-with-rxset_value)
- **[12. Routing and Navigation](#12-routing-and-navigation)**
  - [12.1 Static, dynamic and catch-all routes](#121-static-dynamic-and-catch-all-routes)
  - [12.2 Navigating](#122-navigating)
  - [12.3 Navbar with active-link highlight](#123-navbar-with-active-link-highlight)
  - [12.4 Avoiding the "blank flash" before the app is ready](#124-avoiding-the-blank-flash-before-the-app-is-ready)
- **[13. Tables, Charts and Data Display](#13-tables-charts-and-data-display)**
  - [13.1 Tables](#131-tables)
  - [13.2 Quick data grid with `rx.data_table`](#132-quick-data-grid-with-rxdata_table)
  - [13.3 Charts with Recharts](#133-charts-with-recharts)
  - [13.4 Plotly](#134-plotly)
  - [13.5 Other data-display components](#135-other-data-display-components)
- **[14. Database with `rx.Model`](#14-database-with-rxmodel)**
  - [14.1 Configure the database](#141-configure-the-database)
  - [14.2 Define models](#142-define-models)
  - [14.3 CRUD in a State](#143-crud-in-a-state)
  - [14.4 Migrations](#144-migrations)
- **[15. Browser Storage and Cookies](#15-browser-storage-and-cookies)**
- **[16. Authentication Patterns](#16-authentication-patterns)**
  - [16.1 Models](#161-models)
  - [16.2 Auth state](#162-auth-state)
  - [16.3 Guarding a page](#163-guarding-a-page)
- **[17. File Upload, Download and Assets](#17-file-upload-download-and-assets)**
  - [17.1 Upload](#171-upload)
  - [17.2 Download](#172-download)
  - [17.3 Static assets](#173-static-assets)
- **[18. Backend API and Lifespan Tasks](#18-backend-api-and-lifespan-tasks)**
  - [18.1 Adding your own HTTP endpoints](#181-adding-your-own-http-endpoints)
  - [18.2 Background jobs for the whole server (lifespan tasks)](#182-background-jobs-for-the-whole-server-lifespan-tasks)
  - [18.3 Calling external APIs from handlers](#183-calling-external-apis-from-handlers)
  - [18.4 Exception handling and other settings](#184-exception-handling-and-other-settings)
- **[19. Custom Components](#19-custom-components)**
  - [19.1 Function components (simplest)](#191-function-components-simplest)
  - [19.2 `rx.memo` (performance-optimized reusable components)](#192-rxmemo-performance-optimized-reusable-components)
  - [19.3 Stateful reusable components with `rx.ComponentState`](#193-stateful-reusable-components-with-rxcomponentstate)
  - [19.4 Wrapping a React library](#194-wrapping-a-react-library)
  - [19.5 JavaScript interop](#195-javascript-interop)
- **[20. Configuration and Plugins](#20-configuration-and-plugins)**
- **[21. Testing with Playwright](#21-testing-with-playwright)**
  - [21.1 Make elements easy to find](#211-make-elements-easy-to-find)
  - [21.2 A pytest fixture that starts the app](#212-a-pytest-fixture-that-starts-the-app)
  - [21.3 The tests](#213-the-tests)
  - [21.4 Tips](#214-tips)
- **[22. Deployment and Scaling](#22-deployment-and-scaling)**
  - [22.1 Production build](#221-production-build)
  - [22.2 Options at a glance](#222-options-at-a-glance)
  - [22.3 A starting-point Dockerfile](#223-a-starting-point-dockerfile)
  - [22.4 Scaling checklist](#224-scaling-checklist)
- **[23. Performance and Best Practices](#23-performance-and-best-practices)**
- **[24. Common Errors and Gotchas](#24-common-errors-and-gotchas)**
  - [Gotcha list](#gotcha-list)
- **[25. Full Example Projects](#25-full-example-projects)**
  - [25.1 Todo app (state only, computed vars, filters)](#251-todo-app-state-only-computed-vars-filters)
  - [25.2 Streaming chat with a local or hosted LLM](#252-streaming-chat-with-a-local-or-hosted-llm)
- **[26. Cheat Sheet and Resources](#26-cheat-sheet-and-resources)**
  - [26.1 "I want to…" cheat sheet](#261-i-want-to-cheat-sheet)
  - [26.2 Handy links](#262-handy-links)
  - [26.3 Suggested learning path](#263-suggested-learning-path)

### Quick-Reference Tables Index

Jump straight to the tables of methods, arguments and one-line uses (component catalogs, var operations, route patterns and cheat sheets are included):

- [1.4 What is new in 0.9.x (things that may bite old tutorials)](#14-what-is-new-in-09x-things-that-may-bite-old-tutorials)
- [`reflex` commands](#quick-reference-reflex-commands)
- [`rx.App(...)` arguments](#quick-reference-rxapp-arguments)
- [`rx.App` methods](#quick-reference-rxapp-methods)
- [`app.add_page(...)` arguments](#quick-reference-appadd_page-arguments)
- [6.2 Layout components](#62-layout-components)
- [6.3 Text and typography](#63-text-and-typography)
- [6.4 Buttons, icons, images, feedback](#64-buttons-icons-images-feedback)
- [overlay and disclosure components](#quick-reference-overlay-and-disclosure-components)
- [common style shortcuts](#quick-reference-common-style-shortcuts)
- [`rx.theme(...)` arguments](#quick-reference-rxtheme-arguments)
- [`@rx.var` options](#quick-reference-rxvar-options)
- [8.4 Var operations cheat sheet](#84-var-operations-cheat-sheet)
- [event triggers](#quick-reference-event-triggers)
- [event actions](#quick-reference-event-actions)
- [special events](#quick-reference-special-events)
- [input components](#quick-reference-input-components)
- [12.1 Static, dynamic and catch-all routes](#121-static-dynamic-and-catch-all-routes)
- [`self.router` (read inside handlers)](#quick-reference-selfrouter-read-inside-handlers)
- [table parts](#quick-reference-table-parts)
- [chart types](#quick-reference-chart-types)
- [session and query methods](#quick-reference-session-and-query-methods)
- [storage var types](#quick-reference-storage-var-types)
- [`rx.upload` and helpers](#quick-reference-rxupload-and-helpers)
- [wrapping attributes](#quick-reference-wrapping-attributes)
- [common `rx.Config` options](#quick-reference-common-rxconfig-options)
- [built-in plugins](#quick-reference-built-in-plugins)
- [21.4 Tips](#214-tips)
- [22.2 Options at a glance](#222-options-at-a-glance)
- [23. Performance and Best Practices](#23-performance-and-best-practices)
- [error → fix](#quick-reference-error--fix)
- [26.1 "I want to…" cheat sheet](#261-i-want-to-cheat-sheet)


[↑ Back to top](#table-of-contents)

---

## 1. Introduction and How Reflex Works

### 1.1 What is Reflex?

Reflex is an open-source Python framework where you describe your **UI as Python functions** and your **app logic as Python classes**. Reflex compiles the UI into a React app and runs your logic on a Python backend, keeping the two in sync automatically.

You get:

- **Components** — buttons, inputs, tables, charts, layouts (hundreds built in, based on Radix Themes, Recharts, etc.).
- **State** — a Python class holding your data. When it changes, the UI updates.
- **Events** — Python methods triggered by clicks, typing, page loads, timers.
- **Batteries** — routing, database (SQLModel), file upload, auth patterns, theming, deployment.

### 1.2 Architecture in one picture

```
 ┌───────────────────────────┐   websocket (socket.io)   ┌────────────────────────────┐
 │  BROWSER                  │ ────── events ──────────► │  PYTHON BACKEND (ASGI)     │
 │  React app (compiled from │                           │  • one State tree per tab  │
 │  your Python components)  │ ◄───── state deltas ───── │  • runs your event handlers│
 └───────────────────────────┘                           └────────────────────────────┘
```

1. You write `rx.button("+", on_click=State.increment)`.
2. On `reflex run`, Reflex compiles your components into a React project in the hidden `.web/` folder and starts a dev server (port `3000`) plus the Python backend (port `8000`).
3. A click sends an **event** over a websocket to the backend.
4. Your Python **event handler** runs and changes the **State**.
5. Reflex sends only the **changed values (a "delta")** back; React re-renders what changed.

> **Key mental model:** *State is on the server. The browser is only a view.* Your Python code (including secrets and DB access) never ships to the browser.

### 1.3 The three core ideas

| Concept | What it is | Example |
|---|---|---|
| **Component** | A function returning UI | `def index(): return rx.text("Hi")` |
| **State** | A class that holds app data | `class State(rx.State): count: int = 0` |
| **Event handler** | A State method triggered by the UI | `def increment(self): self.count += 1` |

### 1.4 What is new in 0.9.x (things that may bite old tutorials)

| Change | Since | What you should do |
|---|---|---|
| `pip install reflex` **no longer installs pydantic** | 0.9.9 | Use `pip install "reflex[pydantic]"` or `"reflex[db]"` if you use `rx.Base` / `rx.Model` |
| Frontend uses **React Router 8** and needs **Node ≥ 22.22** | 0.9.9 | Update Node; in custom components use library `react-router` instead of `react-router-dom` |
| `rx.memo` is now first-class (replaces `rx._x.memo`) | 0.9.4 | Annotate params as `rx.Var[...]` and return type as `rx.Component` |
| `rx._x.hybrid_property` (experimental) | 0.9.4 | Same property works on backend and as a frontend var |
| New `preview` run mode (`reflex run --env preview`) | 0.9.8 | Fast rebuilds with an un-minified bundle |
| `rx.asset(...)` URLs are content-hashed | 0.9.8 | Better cache busting, nothing to change |
| `default_color_mode` config option | 0.9.7 | Set light/dark/system without loading large theme CSS |
| `App.hydrate_fallback` | 0.9.5 | Show a loader instead of a blank page while the app hydrates |
| One `rx.App()` per process (uses `RegistrationContext`) | 0.9.9 | Only matters for advanced multi-app tests |
| `REFLEX_LOG_JSON` / `reflex --json` | 0.9.9 | Machine-readable logs |
| `reflex[testing]` extra for `AppHarness` | 0.9.11 | `pip install "reflex[testing]"` for Reflex's test harness |
| Old auto-generated `set_<var>` setters | deprecated | Write explicit setter handlers (see [State](#8-state-and-vars)) |

Also: `reflex init` now writes a Reflex section into `AGENTS.md` (and a `CLAUDE.md` that imports it) so AI coding agents know the project conventions.

[↑ Back to top](#table-of-contents)

---

## 2. Installation and Project Setup

### 2.1 Requirements

- **Python 3.10+** (check the docs for the current minimum), `pip` or `uv`.
- **Node.js ≥ 22.22** (Reflex installs the JS tooling it needs, but Node must be present on recent versions).

### 2.2 Create a project

```bash
mkdir my_app && cd my_app
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install reflex
reflex init                      # choose "blank app"
reflex run                       # open http://localhost:3000
```

Using `uv` instead:

```bash
uv init my_app && cd my_app
uv add reflex
uv run reflex init
uv run reflex run
```

**How it works:** `reflex init` creates the project skeleton and installs frontend dependencies; `reflex run` compiles and starts both servers with **hot reload** (save a `.py` file and the browser updates).

### 2.3 Project structure

```
my_app/
├── .web/                 # generated React project — never edit, add to .gitignore
├── assets/               # static files, served from "/" (favicon, images, css)
├── my_app/
│   ├── __init__.py
│   └── my_app.py         # main module — MUST define a variable named `app`
├── rxconfig.py           # project configuration (see Configuration section)
├── requirements.txt
└── reflex.lock/          # frontend dependency lockfile (recent versions) — commit it
```

Recommended structure once the app grows:

```
my_app/
├── my_app.py             # creates `app`, imports pages
├── state.py              # State classes
├── models.py             # database models
├── components/           # reusable UI pieces (navbar.py, footer.py ...)
└── pages/                # one file per page (index.py, about.py, dashboard.py ...)
```

### 2.4 The two rules Reflex enforces

1. The folder `my_app/` and the file `my_app/my_app.py` must match `app_name` in `rxconfig.py`.
2. `my_app.py` must expose `app = rx.App()`.

[↑ Back to top](#table-of-contents)

---

## 3. CLI Quick Reference

### Quick reference: `reflex` commands

| Command | What it does | Handy flags |
|---|---|---|
| `reflex init` | Scaffold a project in the current folder | `reflex init --help` for template options |
| `reflex run` | Compile + start frontend and backend | `--env dev\|prod\|preview`, `--frontend-only`, `--backend-only`, `--frontend-port 3001`, `--backend-port 8001`, `--backend-host 0.0.0.0`, `--loglevel debug`, `--single-port`, `--json` |
| `reflex export` | Build deployable bundles | `--frontend-only`, `--backend-only`, `--no-zip` |
| `reflex db init` | Set up Alembic migrations for your models | — |
| `reflex db makemigrations` | Generate a migration from model changes | `--message "add note table"` |
| `reflex db migrate` | Apply migrations to the database | — |
| `reflex rename <new_name>` | Rename the app/package | — |
| `reflex login` / `reflex logout` | Sign in/out of Reflex Cloud | — |
| `reflex deploy` | Deploy to Reflex Cloud (or a connected GCP account) | `--provider`, `--description`, `--min-instances`, `--max-instances` |
| `reflex cloud ...` | Manage cloud apps (e.g. `reflex cloud apps history`) | — |
| `reflex component init\|build\|share` | Create and publish custom component packages | — |
| `reflex --version` | Print installed version | — |

**Run modes explained**

| `--env` | Use for | Behavior |
|---|---|---|
| `dev` (default) | Local development | Vite dev server, hot reload |
| `preview` | Faster rebuilds, readable output | Hot reload but serves a freshly built, un-minified bundle |
| `prod` | Production | Optimized build served with the backend |

[↑ Back to top](#table-of-contents)

---

## 4. Your First App

### 4.1 A counter (the "hello world" of Reflex)

```python
import reflex as rx


class State(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count += 1

    @rx.event
    def decrement(self):
        self.count -= 1


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Counter", size="8"),
            rx.heading(State.count),
            rx.hstack(
                rx.button("-", on_click=State.decrement),
                rx.button("+", on_click=State.increment),
            ),
            align="center",
            spacing="4",
        )
    )


app = rx.App()
app.add_page(index)
```

**How it works (line by line)**

- `class State(rx.State)` — your app's data lives here. `count: int = 0` declares a **var** with a type and default. **Type annotations are required.**
- `@rx.event` — marks a method as an **event handler**. (It is recommended for clarity and type checking; plain methods also work.)
- `self.count += 1` — changing a var is all you do. Reflex notices and pushes the update to the browser.
- `index()` — a **page function**; it returns components. Components nest by passing children as positional arguments.
- `rx.heading(State.count)` — passing `State.count` (a var, not `self.count`) makes the heading **reactive**: it re-renders whenever `count` changes.
- `on_click=State.increment` — wires the button to the handler (note: no parentheses; you pass the handler, not call it).
- `rx.vstack` / `rx.hstack` — vertical / horizontal stacks. `align`, `spacing` are props (keyword arguments).
- `app = rx.App()` and `app.add_page(index)` — registers `index` at route `/`.

> **Golden rule:** inside **State methods** use `self.count` (a real Python int). Inside **components** use `State.count` (a placeholder *Var* that becomes a live JavaScript expression in the browser). Never use `self.` inside a component function and never call plain Python functions (`len`, `if`, `for`) on a Var — see [Common Errors](#24-common-errors-and-gotchas).


[↑ Back to top](#table-of-contents)

---

## 5. The App Object and Pages

### 5.1 `rx.App`

`rx.App` is the root object. You create it once, in your main module, and register pages on it.

```python
app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="violet"),
    style={"font_family": "Inter, sans-serif"},
    stylesheets=["https://fonts.googleapis.com/css2?family=Inter&display=swap"],
    head_components=[rx.el.link(rel="icon", href="/favicon.ico")],
)
```

**How it works:** `theme` sets global look (see [Styling](#7-styling-and-theming)); `style` sets default CSS for everything; `stylesheets` loads extra CSS (URLs or files from `assets/`); `head_components` inject tags into `<head>`.

### Quick reference: `rx.App(...)` arguments

| Argument | Type | Purpose |
|---|---|---|
| `theme` | `rx.theme(...)` | Global Radix theme (colors, radius, dark/light) |
| `style` | `dict` | Global style; can target component types, e.g. `{rx.button: {...}}` |
| `stylesheets` | `list[str]` | Extra CSS files/URLs (files live in `assets/`, referenced as `"/my.css"`) |
| `head_components` | `list[Component]` | Extra tags in `<head>` (fonts, analytics, meta) |
| `overlay_component` | `Component` | Component rendered on top of every page (e.g. connection-lost banner) |
| `toaster` | `rx.toast.provider(...)` | Configure the toast notification host |
| `html_lang` | `str` | `<html lang="...">` value |
| `html_custom_attrs` | `dict` | Extra attributes on `<html>` |
| `api_transformer` | ASGI/FastAPI app or callable | Mount your own API routes into the backend (see [Backend API](#18-backend-api-and-lifespan-tasks)) |
| `hydrate_fallback` | `Component` | Shown while the page hydrates (instead of a blank page) |
| `admin_dash` | `rx.AdminDash(models=[...])` | Built-in admin dashboard for your DB models |

### Quick reference: `rx.App` methods

| Method | Purpose |
|---|---|
| `app.add_page(component, route=..., ...)` | Register a page |
| `app.register_lifespan_task(async_fn)` | Run a background coroutine for the life of the server |

### 5.2 Adding pages

```python
def index() -> rx.Component:
    return rx.heading("Home")

def about() -> rx.Component:
    return rx.heading("About us")

app = rx.App()
app.add_page(index)                                   # route "/"
app.add_page(about, route="/about", title="About")   # route "/about"
```

**How it works:** the **function name** becomes the route (`about` → `/about`), except `index` which is `/`. Override with `route=`. Pass the function itself — do not call it.

### Quick reference: `app.add_page(...)` arguments

| Argument | Purpose |
|---|---|
| `component` | Page function (or component) to render |
| `route` | URL path. Supports dynamic parts: `/user/[id]`, catch-all `/docs/[...slug]` |
| `title` | Browser tab title |
| `description` | `<meta name="description">` for SEO |
| `image` | Preview image (Open Graph) |
| `on_load` | Event handler(s) to run when the page loads (fetch data, auth check) |
| `meta` | List of extra meta tags, e.g. `[{"name": "theme-color", "content": "#000"}]` |

### 5.3 The `@rx.page` decorator (same thing, less boilerplate)

```python
@rx.page(route="/dashboard", title="Dashboard", on_load=DashState.load)
def dashboard() -> rx.Component:
    return rx.heading("Dashboard")
```

**How it works:** the decorator registers the page for you. `@rx.page` accepts the same options as `add_page` (`route`, `title`, `description`, `image`, `on_load`, `meta`). **Gotcha:** the module containing the decorated page must be *imported* from your main file, otherwise the page never registers:

```python
# my_app/my_app.py
import reflex as rx
from .pages import dashboard, about   # noqa: F401  (import registers the pages)

app = rx.App()
```

### 5.4 A custom 404 page

```python
@rx.page(route="/404", title="Not found")
def not_found() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("404", size="9"),
            rx.text("That page does not exist."),
            rx.link("Go home", href="/"),
        ),
        height="100vh",
    )
```

**How it works:** Reflex uses the page registered at `/404` whenever no route matches.

### 5.5 A shared page template

Wrap every page with a navbar/footer with a small decorator:

```python
import functools

def template(page):
    @functools.wraps(page)              # keeps the function name -> route stays correct
    def wrapper() -> rx.Component:
        return rx.vstack(
            navbar(),
            rx.container(page(), width="100%"),
            footer(),
            width="100%",
            spacing="0",
        )
    return wrapper

@rx.page(route="/pricing")
@template
def pricing() -> rx.Component:
    return rx.heading("Pricing")
```

**How it works:** `template` takes a page function, returns a new function that builds the same page inside a layout. Decorators stack bottom-up: first `template`, then `rx.page`.

[↑ Back to top](#table-of-contents)

---

## 6. Components

### 6.1 Anatomy of a component

```python
rx.button(
    "Save",                       # positional args = children
    color_scheme="green",         # keyword args = props
    variant="soft",
    on_click=State.save,          # event triggers are props too
)
```

- **Children** are positional arguments (text, other components, Vars).
- **Props** are keyword arguments. CSS properties can be passed the same way (`padding="1em"`).
- Everything returns an `rx.Component`, so you can build your own functions that return components and reuse them.

```python
def stat_card(label: str, value: str) -> rx.Component:
    return rx.card(rx.vstack(rx.text(label, size="2"), rx.heading(value)))

rx.hstack(stat_card("Users", "1,204"), stat_card("Revenue", "$9.4k"))
```

**How it works:** your own components are plain functions — no registration needed. For **state-bound** values pass a Var, e.g. `stat_card("Users", State.user_count)` (then type the argument as `rx.Var[str]` or leave it untyped).

### 6.2 Layout components

| Component | Purpose | Key props |
|---|---|---|
| `rx.box` | Generic container (`<div>`) | any CSS prop |
| `rx.flex` | Flexbox | `direction`, `align`, `justify`, `wrap`, `spacing` |
| `rx.vstack` / `rx.hstack` | Vertical / horizontal flex | `spacing`, `align`, `justify`, `wrap` |
| `rx.center` | Centers children | — |
| `rx.grid` | CSS grid | `columns="3"`, `rows`, `spacing`, `flow` |
| `rx.container` | Max-width centered page wrapper | `size="1"…"4"` |
| `rx.section` | Vertical page section spacing | `size` |
| `rx.spacer` | Flexible gap (pushes siblings apart) | — |
| `rx.separator` | Divider line | `orientation`, `size` |
| `rx.card` | Bordered surface | `variant`, `size` |
| `rx.inset` | Full-bleed content inside a card | `side`, `clip` |
| `rx.scroll_area` | Custom scroll container | `type`, `scrollbars`, `height` |
| `rx.aspect_ratio` | Keep a fixed ratio (e.g. for video) | `ratio=16/9` |
| `rx.fragment` | Group without an extra DOM node | — |
| `rx.desktop_only` / `rx.tablet_only` / `rx.mobile_only` | Show only on that screen size | — |
| `rx.mobile_and_tablet` / `rx.tablet_and_desktop` | Combined breakpoints | — |

```python
rx.grid(
    rx.card("A"), rx.card("B"), rx.card("C"), rx.card("D"),
    columns="2",
    spacing="4",
    width="100%",
)
```

**How it works:** `columns="2"` makes a 2-column grid; the four cards wrap into two rows. `width="100%"` makes the grid fill its parent.

### 6.3 Text and typography

| Component | Purpose | Key props |
|---|---|---|
| `rx.heading` | Titles | `size="1"…"9"`, `as_="h1"`, `weight`, `align` |
| `rx.text` | Paragraph / inline text | `size`, `weight`, `color_scheme`, `align`, `as_="span"` |
| `rx.code` | Inline code | `size`, `variant` |
| `rx.code_block` | Highlighted code block | `code`, `language`, `show_line_numbers` |
| `rx.markdown` | Render a Markdown string (great for LLM output) | pass the string as child |
| `rx.link` | Hyperlink | `href`, `is_external=True` |
| `rx.blockquote` | Quote | — |
| `rx.strong`, `rx.em`, `rx.kbd` | Emphasis, italics, keyboard key | — |
| `rx.badge` | Small label | `color_scheme`, `variant` |
| `rx.callout` | Notice box | `icon`, `color_scheme`, text as child |

```python
rx.vstack(
    rx.heading("Welcome", size="7"),
    rx.text("Reflex is ", rx.strong("pure Python"), ".", color_scheme="gray"),
    rx.code_block("print('hi')", language="python"),
    rx.callout("Saved successfully", icon="check", color_scheme="green"),
)
```

**How it works:** components nest: `rx.text` receives plain strings and another component (`rx.strong`) as children. `icon="check"` uses a **Lucide** icon by name.

### 6.4 Buttons, icons, images, feedback

| Component | Purpose | Key props |
|---|---|---|
| `rx.button` | Button | `variant="solid\|soft\|outline\|ghost\|surface"`, `size="1"…"4"`, `color_scheme`, `loading`, `disabled`, `on_click` |
| `rx.icon_button` | Icon-only button | wrap `rx.icon("plus")` |
| `rx.icon` | Lucide icon | `tag="search"`, `size=20`, `color` |
| `rx.image` | Image | `src="/logo.png"`, `alt`, `width`, `height` |
| `rx.avatar` | Profile picture | `src`, `fallback="HV"`, `size` |
| `rx.progress` | Progress bar | `value=60` |
| `rx.spinner` | Loading spinner | `loading=True`, `size` |
| `rx.skeleton` | Placeholder while loading | `loading` |
| `rx.tooltip` | Hover hint | `content="Tip"` wrapping a child |
| `rx.toast(...)` | Pop-up notification (an *event*, returned from handlers) | see [Special events](#quick-reference-special-events) |

```python
rx.hstack(
    rx.button("Save", loading=State.saving, on_click=State.save),
    rx.icon_button(rx.icon("trash-2"), color_scheme="red", variant="soft"),
    rx.avatar(fallback="HV", size="3"),
    rx.tooltip(rx.badge("Beta"), content="This feature is in beta"),
)
```

**How it works:** `loading=State.saving` binds the spinner state of the button to a bool var — the button shows a spinner and disables itself whenever `saving` is `True`.

### 6.5 Overlays and navigation widgets

**Dialog (modal)**

```python
rx.dialog.root(
    rx.dialog.trigger(rx.button("Open")),
    rx.dialog.content(
        rx.dialog.title("Hello"),
        rx.dialog.description("This is a modal dialog."),
        rx.dialog.close(rx.button("Close")),
    ),
)
```

**How it works:** Radix-style compound components — `root` holds state, `trigger` opens it, `content` is the modal, `close` closes it. No State class needed for simple cases.

**Tabs**

```python
rx.tabs.root(
    rx.tabs.list(
        rx.tabs.trigger("Account", value="account"),
        rx.tabs.trigger("Billing", value="billing"),
    ),
    rx.tabs.content(rx.text("Account settings"), value="account"),
    rx.tabs.content(rx.text("Billing settings"), value="billing"),
    default_value="account",
)
```

**How it works:** each `trigger` and `content` share a `value`; `default_value` picks the initially visible tab.

**Accordion**

```python
rx.accordion.root(
    rx.accordion.item(header="What is Reflex?", content="A Python web framework."),
    rx.accordion.item(header="Is it free?", content="The framework is open source."),
    type="single",
    collapsible=True,
    variant="soft",
)
```

**Dropdown menu**

```python
rx.menu.root(
    rx.menu.trigger(rx.button("Actions")),
    rx.menu.content(
        rx.menu.item("Edit", on_click=State.edit),
        rx.menu.separator(),
        rx.menu.item("Delete", color="red", on_click=State.delete),
    ),
)
```

### Quick reference: overlay and disclosure components

| Component family | Parts | Typical use |
|---|---|---|
| `rx.dialog` | `root`, `trigger`, `content`, `title`, `description`, `close` | Modals / forms in popups |
| `rx.alert_dialog` | same shape, plus `action`, `cancel` | "Are you sure?" confirmations |
| `rx.popover` | `root`, `trigger`, `content`, `close` | Small floating panels |
| `rx.hover_card` | `root`, `trigger`, `content` | Preview on hover |
| `rx.menu` (dropdown) | `root`, `trigger`, `content`, `item`, `separator`, `sub` | Action menus |
| `rx.context_menu` | `root`, `trigger`, `content`, `item` | Right-click menu |
| `rx.tabs` | `root`, `list`, `trigger`, `content` | Tabbed content |
| `rx.accordion` | `root`, `item` | Collapsible FAQ |
| `rx.drawer` | `root`, `trigger`, `overlay`, `portal`, `content`, `close` | Side / bottom sheet |
| `rx.segmented_control` | `root`, `item` | Compact mode switch |
| `rx.data_list` | `root`, `item`, `label`, `value` | Key/value lists |

### 6.6 Raw HTML elements with `rx.el`

```python
rx.el.div(
    rx.el.h1("Plain HTML heading"),
    rx.el.a("Docs", href="https://reflex.dev", target="_blank"),
    class_name="p-4",            # class_name works with Tailwind (see Styling)
)
```

**How it works:** `rx.el.<tag>` maps 1:1 to HTML elements (`div`, `span`, `a`, `button`, `input`, `img`, `ul`, `li`, `svg`, ...). Use them when you need exact HTML, or when you use Tailwind classes. For raw HTML strings use `rx.html("<b>hi</b>")` (only with trusted content!).

[↑ Back to top](#table-of-contents)

---

## 7. Styling and Theming

### 7.1 Style props (CSS as keyword arguments)

```python
rx.box(
    "Styled box",
    padding="1.5em",
    bg="#111827",                       # bg = background
    color="white",
    border_radius="12px",
    width="100%",
    max_width="480px",
    box_shadow="0 4px 16px rgba(0,0,0,.25)",
    _hover={"bg": "#1f2937", "cursor": "pointer"},
)
```

**How it works:** any CSS property in `snake_case` is accepted (`font_size`, `border_radius`, `margin_top`). Pseudo-classes use a leading underscore: `_hover`, `_focus`, `_active`, `_disabled`, `_before`, `_after`.

### Quick reference: common style shortcuts

| Prop | Meaning | Example |
|---|---|---|
| `p`, `px`, `py`, `pt`, `pb`, `pl`, `pr` / `padding` | Padding | `p="4"` (theme scale) or `padding="1em"` |
| `m`, `mx`, `my`, `mt`, `mb`, `ml`, `mr` / `margin` | Margin | `mx="auto"` |
| `width`, `height`, `min_width`, `max_width` | Size | `width="100%"` |
| `bg` / `background` | Background | `bg=rx.color("accent", 3)` |
| `color` | Text color | `color="white"` |
| `display`, `flex`, `gap`, `align_items`, `justify_content` | Layout | `display="flex"` |
| `border`, `border_radius` | Border | `border="1px solid gray"` |
| `position`, `top`, `left`, `z_index` | Positioning | `position="fixed"` |
| `overflow`, `overflow_x`, `overflow_y` | Scrolling | `overflow_x="auto"` |
| `_hover`, `_focus`, `_active`, `_disabled` | State styles | `_hover={"opacity": 0.8}` |

### 7.2 Responsive design

**Option A — a list, one value per breakpoint** (`initial`, `xs`, `sm`, `md`, `lg`, `xl`):

```python
rx.box(
    "Responsive",
    width=["100%", "100%", "75%", "50%"],
)
```

**Option B — explicit names:**

```python
rx.box("Responsive", width=rx.breakpoints(initial="100%", sm="75%", lg="50%"))
```

**Option C — show/hide entire blocks:**

```python
rx.fragment(
    rx.mobile_only(mobile_menu()),
    rx.tablet_and_desktop(desktop_menu()),
)
```

**How it works:** Reflex generates media queries from the list/breakpoints. Smaller screens fall back to the value of the previous breakpoint.

### 7.3 Global and per-component-type styles

```python
app = rx.App(
    style={
        "font_family": "Inter, sans-serif",
        rx.heading: {"letter_spacing": "-0.02em"},          # every rx.heading
        rx.button: {"cursor": "pointer"},                   # every rx.button
    },
    stylesheets=["/global.css"],                            # assets/global.css
)
```

### 7.4 Themes (`rx.theme`)

```python
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="indigo",
        gray_color="slate",
        radius="large",
        scaling="100%",
        panel_background="translucent",
    )
)
```

### Quick reference: `rx.theme(...)` arguments

| Argument | Values | Effect |
|---|---|---|
| `appearance` | `"light"`, `"dark"`, `"inherit"` | Base mode |
| `accent_color` | `"indigo"`, `"violet"`, `"crimson"`, `"grass"`, `"orange"`, … | Primary color used by buttons, links, focus rings |
| `gray_color` | `"gray"`, `"slate"`, `"sand"`, `"mauve"`, … | Neutral color tone |
| `radius` | `"none"`, `"small"`, `"medium"`, `"large"`, `"full"` | Corner roundness |
| `scaling` | `"90%"`, `"95%"`, `"100%"`, `"105%"`, `"110%"` | Global UI scale |
| `has_background` | `bool` | Whether theme paints the page background |
| `panel_background` | `"solid"`, `"translucent"` | Card/dialog surface style |

**Tip:** add `rx.theme_panel()` to any page during development to tweak the theme live, then copy the values into `rx.theme(...)`.

### 7.5 Colors

```python
rx.text("Accent text", color=rx.color("accent", 11))
rx.box(bg=rx.color("gray", 3), border=f"1px solid {rx.color('gray', 6)}")
```

**How it works:** `rx.color(name, shade)` picks from Radix's 12-step color scales (1 = lightest background … 12 = high-contrast text). Using these instead of hard-coded hex values means your app automatically works in light **and** dark mode.

### 7.6 Dark / light mode

```python
rx.hstack(
    rx.color_mode.button(),                                    # ready-made toggle
    rx.color_mode_cond(light=rx.icon("sun"), dark=rx.icon("moon")),  # show different UI per mode
    rx.button("Toggle", on_click=rx.toggle_color_mode),        # custom toggle
)
```

Set the initial mode without loading the full theme CSS via config: `rx.Config(app_name="my_app", default_color_mode="dark")` (`"system"`, `"light"` or `"dark"`).

### 7.7 Tailwind CSS (optional)

```python
# rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="my_app",
    plugins=[rx.plugins.TailwindV4Plugin()],
)
```

```python
rx.el.div("Tailwind!", class_name="p-4 rounded-xl bg-indigo-600 text-white")
```

**How it works:** enabling the plugin adds Tailwind to the build; then use `class_name` on any component (`rx.box`, `rx.el.*`).


[↑ Back to top](#table-of-contents)

---

## 8. State and Vars

### 8.1 Defining state

```python
class ProfileState(rx.State):
    name: str = ""
    age: int = 0
    active: bool = True
    tags: list[str] = []
    prefs: dict[str, str] = {}
```

**How it works:** every attribute with a **type annotation and default** becomes a **var** — a piece of data that lives on the server for each browser session and is mirrored to the UI. Reflex creates a **separate copy of the state for each browser tab** (each identified by a client token), so users never see each other's data.

**Rules for vars**

| Rule | Why |
|---|---|
| Always add a type annotation | Reflex needs the type to generate the frontend code |
| Values must be JSON-serializable (str, int, float, bool, list, dict, dataclass, datetime, …) | They are sent to the browser |
| Names starting with `_` are **backend-only** vars | They are never sent to the browser |
| Don't reuse built-in names (`router`, `dict`, `reset`, `get_state` …) | They belong to `rx.State` |
| Public methods on a State are treated as event handlers | Put helpers behind `_underscore` names |

### 8.2 Backend-only vars (private)

```python
class ApiState(rx.State):
    result: str = ""                 # frontend var (sent to browser)
    _api_key: str = "sk-..."         # backend var (never leaves the server)
    _cache: dict = {}                # good place for big/temporary data
```

**How it works:** the leading underscore keeps the var on the server. Use it for secrets, caches, and large data you don't want to serialize to the browser on every update. You **cannot** reference a backend var in a component (`ApiState._api_key` in UI code is an error) — read it inside handlers only.

### 8.3 Computed vars (`@rx.var`)

```python
class CartState(rx.State):
    prices: list[float] = [9.99, 4.50, 12.00]
    tax_rate: float = 0.18

    @rx.var
    def subtotal(self) -> float:
        return sum(self.prices)

    @rx.var
    def total(self) -> str:
        return f"${self.subtotal * (1 + self.tax_rate):.2f}"
```

```python
rx.text("Total: ", CartState.total)
```

**How it works:** a computed var is a **read-only value derived from other vars**. Reflex recomputes it automatically when a var it depends on changes and pushes the new value to the UI. **The return type annotation is mandatory.** Computed vars are the right place for filtering, sorting, and formatting — because Python `if`/`for`/`len()` do **not** work on Vars inside components (see [Var operations](#84-var-operations-cheat-sheet)).

### Quick reference: `@rx.var` options

| Option | Default | Meaning |
|---|---|---|
| *(none)* `@rx.var` | — | Cached; recomputed only when dependencies change |
| `auto_deps=False` | `True` | Turn off automatic dependency detection (then list them in `deps`) |
| `deps=["field_a", ...]` | `[]` | Manually declare which vars this depends on |
| `interval=5` | `None` | Recompute on a timer (seconds or `datetime.timedelta`) — useful for clocks/"time ago" |
| `initial_value=...` | `None` | Value shown before the first computation |
| `backend=True` | `False` | Backend-only computed var (not sent to browser) |

### 8.4 Var operations cheat sheet

Inside components, `State.something` is a **Var**, not a real Python value. Use these Var-friendly operations:

| You want (Python) | Write this on a Var | Notes |
|---|---|---|
| `len(x)` | `x.length()` | lists, strings |
| `str(x)` | `x.to_string()` | number → text |
| `x + y`, `x - y`, `x * y`, `x / y`, `x % y`, `x ** y` | same operators | numbers; `+` also joins strings |
| `x > y`, `x == y`, `x <= y` | same operators | result is a bool Var |
| `a and b` | `a & b` | logical AND |
| `a or b` | `a \| b` | logical OR |
| `not a` | `~a` | logical NOT |
| `if a: ... else: ...` | `rx.cond(a, yes, no)` | see [Conditional rendering](#10-conditional-rendering-and-loops) |
| `for i in items:` | `rx.foreach(items, render_fn)` | see [Loops](#103-loops-with-rxforeach) |
| `item in my_list` | `my_list.contains(item)` | also works for strings / dict keys |
| `", ".join(my_list)` | `my_list.join(", ")` | |
| `my_list[::-1]` | `my_list.reverse()` | |
| `text.upper()`, `.lower()`, `.split(",")` | same names | string Vars |
| `my_list[0]`, `my_dict["k"]` | same indexing | dict/list Vars |
| `f"Hi {State.name}"` | f-strings work | Vars interpolate into strings |
| `round(x)` | `x.round()` | number Vars |

```python
rx.vstack(
    rx.text(f"You have {CartState.prices.length()} items"),
    rx.cond(CartState.prices.length() > 0, rx.text("Ready to pay"), rx.text("Cart empty")),
)
```

### 8.5 Mutable vars (lists, dicts, sets)

```python
class ListState(rx.State):
    items: list[str] = []
    scores: dict[str, int] = {}

    @rx.event
    def add(self, text: str):
        self.items.append(text)          # in-place mutation is detected
        self.scores[text] = len(text)    # also detected

    @rx.event
    def clear(self):
        self.items = []                  # re-assignment always works
```

**How it works:** Reflex wraps mutable vars in a proxy so in-place changes (`append`, `pop`, `d[k] = v`) mark the var as "dirty". If you ever mutate something Reflex can't see (e.g. an object stored *inside* a non-Reflex class), **re-assign** the var (`self.items = list(self.items)`) to force an update.

### 8.6 Custom types with dataclasses

```python
import dataclasses

@dataclasses.dataclass
class Person:
    name: str
    age: int


class PeopleState(rx.State):
    people: list[Person] = [Person("Ada", 36), Person("Linus", 55)]


def person_row(p: Person) -> rx.Component:      # annotate the item type!
    return rx.text(p.name, " is ", p.age)


rx.foreach(PeopleState.people, person_row)
```

**How it works:** a dataclass gives typed fields you can read in components (`p.name`). Annotating the render function's parameter (`p: Person`) lets Reflex know which attributes exist. (`rx.Base` — a pydantic-based class — also works but needs the `reflex[pydantic]` extra in 0.9.9+; prefer dataclasses.)

### 8.7 Substates and inheritance

```python
class BaseState(rx.State):
    username: str = "guest"          # shared by children

class SettingsState(BaseState):      # child "substate"
    theme: str = "light"

    @rx.event
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        # self.username is available too (inherited)
```

**How it works:** every class that inherits from `rx.State` is a node in a **state tree**. Children can read/write their parent's vars. Siblings cannot see each other directly.

**Reading another state from a handler** — use `get_state` (the handler must be `async`):

```python
class CartState(rx.State):
    items: list[str] = []

class CheckoutState(rx.State):
    @rx.event
    async def place_order(self):
        cart = await self.get_state(CartState)
        count = len(cart.items)
        cart.items = []                 # you may modify it too
        return rx.toast.success(f"Ordered {count} items")
```

### 8.8 Resetting and misc state helpers

| Helper | Use |
|---|---|
| `self.reset()` | Reset this state's vars to their defaults (e.g. on logout) |
| `await self.get_state(Other)` | Get another state instance (async handler) |
| `State.is_hydrated` | Var: `True` once the browser has loaded initial state |
| `self.router` | Info about the current URL/session (see [Routing](#12-routing-and-navigation)) |
| `self.dict()` | State vars as a dict (debugging) |

### 8.9 Setters — write them explicitly

```python
class FormState(rx.State):
    name: str = ""

    @rx.event
    def set_name(self, value: str):
        self.name = value
```

```python
rx.input(value=FormState.name, on_change=FormState.set_name)
```

**How it works:** older tutorials rely on automatically generated `set_<var>` methods. Those are **deprecated** in recent versions, so define the tiny handler yourself (as above). A generic alternative exists: `on_change=FormState.setvar("name")`.

[↑ Back to top](#table-of-contents)

---

## 9. Events and Event Handlers

### 9.1 What is an event handler?

A **method on a State class** that changes the state, triggered from the UI. Decorate with `@rx.event` (recommended).

```python
class TodoState(rx.State):
    todos: list[str] = []

    @rx.event
    def add_todo(self, text: str):
        self.todos.append(text)
```

**How it works:** when the UI triggers `add_todo`, Reflex sends a message to the backend, calls the method, collects the changed vars, and returns the delta to the browser.

### 9.2 Passing arguments

```python
rx.button("Add milk", on_click=TodoState.add_todo("milk"))          # fixed argument
rx.input(on_change=TodoState.add_todo)                               # gets the input value
rx.foreach(TodoState.todos, lambda t: rx.button(t, on_click=TodoState.remove(t)))  # per-item
```

**How it works:**

- `State.handler("literal")` — *pre-fills* the argument. You are not calling the method; you're building an event description.
- `on_change=State.handler` — Reflex passes the event's value (the new text) as the first argument.
- Inside `rx.foreach`, item Vars (`t`) can be passed as arguments so each row acts on its own data.
- **Add type hints** to handler parameters (`text: str`, `todo_id: int`); Reflex checks them.

### 9.3 Event triggers (props you attach handlers to)

### Quick reference: event triggers

| Trigger | Fires when | Handler receives |
|---|---|---|
| `on_click` | Element clicked | nothing |
| `on_double_click` | Double click | nothing |
| `on_context_menu` | Right click | nothing |
| `on_mouse_enter` / `on_mouse_leave` | Pointer enters / leaves | nothing |
| `on_mouse_down` / `on_mouse_up` | Pointer pressed / released | nothing |
| `on_change` (`rx.input`, `rx.text_area`) | Text changes (each keystroke) | `str` |
| `on_change` (`rx.select`, `rx.radio_group`) | Selection changes | `str` |
| `on_change` (`rx.checkbox`, `rx.switch`) | Toggled | `bool` |
| `on_change` (`rx.slider`) | Slider moved | `list[float]` |
| `on_value_commit` (`rx.slider`) | Slider released | `list[float]` |
| `on_blur` / `on_focus` | Field loses / gains focus | `str` (blur on inputs) / nothing |
| `on_key_down` / `on_key_up` | Key pressed / released | `str` (key name, e.g. `"Enter"`) |
| `on_submit` (`rx.form`) | Form submitted | `dict` of field values |
| `on_mount` / `on_unmount` | Component appears / disappears | nothing |
| `on_scroll` | Element scrolled | nothing |
| `on_open_change` (dialog, popover) | Opened / closed | `bool` |
| `on_load` (page-level) | Page navigated to | nothing |

### 9.4 Streaming updates with `yield`

```python
import asyncio

class ProgressState(rx.State):
    progress: int = 0

    @rx.event
    async def run_job(self):
        self.progress = 0
        for _ in range(10):
            await asyncio.sleep(0.3)
            self.progress += 10
            yield                        # push the current state to the browser NOW
```

```python
rx.vstack(
    rx.progress(value=ProgressState.progress),
    rx.button("Start", on_click=ProgressState.run_job),
)
```

**How it works:** normally the UI updates when the handler *finishes*. `yield` sends an update immediately and continues, so you get live progress. Prefer `async def` and `await asyncio.sleep()` (or async HTTP calls) for waiting, so you don't block the server.

### 9.5 Chaining events

```python
class FlowState(rx.State):
    saved: bool = False

    @rx.event
    def save(self):
        self.saved = True
        return FlowState.after_save            # run another handler next

    @rx.event
    def after_save(self):
        yield rx.toast.success("Saved!")
        yield rx.redirect("/done")

    @rx.event
    def multiple(self):
        return [FlowState.save, OtherState.refresh]   # a list runs them in order
```

**How it works:** a handler can `return` (or `yield`) another handler, a **special event** (toast, redirect ...), or a **list** of them. This is how you split large flows into small handlers.

### 9.6 Event actions (modifiers)

```python
rx.input(on_change=SearchState.search.debounce(300))          # wait 300 ms after last keystroke
rx.button("Save", on_click=State.save.throttle(1000))         # at most once per second
rx.link("x", on_click=State.track.prevent_default)            # don't follow the link
rx.box(on_click=State.inner.stop_propagation)                 # don't bubble to parents
```

### Quick reference: event actions

| Modifier | Effect |
|---|---|
| `.debounce(ms)` | Only fire after `ms` milliseconds of silence (search-as-you-type) |
| `.throttle(ms)` | Fire at most once per `ms` |
| `.prevent_default` | Cancel the browser's default action |
| `.stop_propagation` | Stop the event from reaching parent elements |
| `.temporal` | Drop the event if the backend is disconnected |

### 9.7 Special events (quick reference)

Return or `yield` these from handlers; they run in the **browser**.

### Quick reference: special events

| Event | What it does | Example |
|---|---|---|
| `rx.redirect(path, is_external=False, replace=False)` | Navigate | `return rx.redirect("/login")` |
| `rx.toast(msg)` / `rx.toast.success/error/warning/info(msg)` | Show a notification | `return rx.toast.error("Oops")` |
| `rx.set_value(id, value)` | Set an input's value by `id` (e.g. clear it) | `return rx.set_value("q", "")` |
| `rx.set_clipboard(text)` | Copy text to the clipboard | `return rx.set_clipboard(State.link)` |
| `rx.download(url=... \| data=..., filename=...)` | Trigger a file download | `return rx.download(data="a,b", filename="x.csv")` |
| `rx.scroll_to(elem_id)` | Scroll an element into view | `return rx.scroll_to("footer")` |
| `rx.window_alert(msg)` | Browser `alert()` | `return rx.window_alert("Hi")` |
| `rx.console_log(msg)` | `console.log` | `return rx.console_log("debug")` |
| `rx.call_script(js, callback=None)` | Run JavaScript (optionally send result to a handler) | `return rx.call_script("navigator.userAgent", State.got_ua)` |
| `rx.remove_cookie(key)` | Delete a cookie | see [Storage](#15-browser-storage-and-cookies) |
| `rx.remove_local_storage(key)` / `rx.clear_local_storage()` | Local storage cleanup | |
| `rx.clear_session_storage()` | Session storage cleanup | |
| `rx.upload_files(...)`, `rx.clear_selected_files(id)` | Upload helpers | see [Uploads](#17-file-upload-download-and-assets) |

### 9.8 Background tasks (long-running work)

```python
import asyncio

class ClockState(rx.State):
    ticks: int = 0
    running: bool = False

    @rx.event(background=True)
    async def start(self):
        async with self:                       # lock the state to READ/WRITE it
            if self.running:
                return
            self.running = True

        while True:
            async with self:
                if not self.running:
                    break
                self.ticks += 1                # update is pushed when the block exits
            await asyncio.sleep(1)             # sleeping OUTSIDE the lock

    @rx.event
    def stop(self):
        self.running = False
```

**How it works:**

- A normal handler **locks the state** for its whole run; other events for that user wait. A `background=True` handler does *not*, so the UI stays responsive.
- It must be `async`. You touch `self` **only inside `async with self:`** — outside the block Reflex raises an error to protect you from race conditions.
- Each time the `async with self:` block ends, changed vars are sent to the browser.
- Ideal for: polling, streaming LLM tokens, long API calls, timers.

### 9.9 Page load and mount events

```python
class DashState(rx.State):
    rows: list[dict] = []

    @rx.event
    async def load(self):
        self.rows = await fetch_rows()

@rx.page(route="/dash", on_load=DashState.load)   # runs whenever the user opens /dash
def dash() -> rx.Component:
    return rx.table.root(...)
```

Use `on_mount` on a **component** to run something when that component appears (e.g. a widget inside a dialog).

[↑ Back to top](#table-of-contents)

---

## 10. Conditional Rendering and Loops

### 10.1 `rx.cond` (if / else)

```python
rx.cond(
    AuthState.logged_in,
    rx.text("Welcome back!"),         # shown when True
    rx.button("Log in"),              # shown when False (optional)
)
```

You can also use it to pick a **prop value**:

```python
rx.box("Status", bg=rx.cond(State.online, "green", "red"))
```

**How it works:** `rx.cond(condition, if_true, if_false)` becomes a JavaScript ternary in the browser. **Both branches are compiled**, so keep them cheap and never put code with side effects in them. Python's `if State.flag:` does **not** work on a Var.

### 10.2 `rx.match` (switch / case)

```python
rx.match(
    OrderState.status,
    ("paid", rx.badge("Paid", color_scheme="green")),
    ("pending", rx.badge("Pending", color_scheme="amber")),
    ("failed", rx.badge("Failed", color_scheme="red")),
    rx.badge("Unknown"),              # last positional arg = default
)
```

**How it works:** the first argument is the value to test; each tuple is `(case, result)`; a final non-tuple is the default.

### 10.3 Loops with `rx.foreach`

```python
class ShopState(rx.State):
    products: list[str] = ["Tea", "Coffee", "Milk"]

def product_item(name: str) -> rx.Component:
    return rx.list.item(name)

rx.list.unordered(rx.foreach(ShopState.products, product_item))
```

With an index:

```python
rx.foreach(ShopState.products, lambda name, i: rx.text(i, ". ", name))
```

Over a dict (yields `[key, value]` pairs):

```python
rx.foreach(State.scores, lambda kv: rx.text(kv[0], ": ", kv[1]))
```

**How it works:**

- The first argument must be a **list Var with a type annotation** (`list[str]`, `list[Person]`).
- The render function receives **one item (a Var)**, and optionally the **index**. It must return a component and **cannot use Python `if`/`for` on the item** — use `rx.cond` inside.
- A plain Python list (not a Var) can just be looped with a normal `for` or a list comprehension at *build time*: `[rx.text(x) for x in ["a", "b"]]`.


[↑ Back to top](#table-of-contents)

---

## 11. Forms and Inputs

### 11.1 A complete form with `on_submit`

```python
class SignupState(rx.State):
    last_submitted: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        self.last_submitted = form_data
        return rx.toast.success(f"Welcome, {form_data['name']}!")


def signup_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(name="name", placeholder="Your name", required=True),
            rx.input(name="email", type="email", placeholder="Email"),
            rx.select(["Free", "Pro", "Team"], name="plan", default_value="Free"),
            rx.text_area(name="bio", placeholder="About you"),
            rx.button("Sign up", type="submit"),
            spacing="3",
        ),
        on_submit=SignupState.handle_submit,
        reset_on_submit=True,
    )
```

**How it works:**

- Each field has a **`name`**. On submit, Reflex gathers all named fields into a `dict` (`{"name": "...", "email": "...", ...}`) and passes it to your handler.
- `required=True`, `type="email"` use the browser's built-in validation before the event is sent.
- `reset_on_submit=True` clears the form afterward.
- This is the **uncontrolled** style: the browser holds the values; the backend only sees them on submit. Best for most forms.
- You can also annotate the handler with a `TypedDict` (`form_data: SignupData`) and Reflex will check at build time that the form provides the required fields.

### 11.2 Controlled inputs (live-bound to state)

```python
class SearchState(rx.State):
    query: str = ""

    @rx.event
    def set_query(self, value: str):
        self.query = value

    @rx.var
    def shout(self) -> str:
        return self.query.upper()


rx.vstack(
    rx.input(
        value=SearchState.query,
        on_change=SearchState.set_query.debounce(200),   # avoid one event per keystroke
        placeholder="Type…",
    ),
    rx.text("You typed: ", SearchState.shout),
)
```

**How it works:** `value=` ties the input to a var; `on_change` writes back. Use this when other parts of the UI must react while the user types (live search, live preview, validation messages).

### Quick reference: input components

| Component | Key props | `on_change` gives |
|---|---|---|
| `rx.input` | `value`, `default_value`, `placeholder`, `type` (`text`, `password`, `email`, `number`…), `name`, `required`, `disabled`, `max_length`, `min_length`, `pattern`, `size`, `variant`, `id` | `str` |
| `rx.text_area` | `value`, `placeholder`, `rows`, `resize`, `name` | `str` |
| `rx.select(items, ...)` | `value`, `default_value`, `placeholder`, `name`, `disabled` | `str` |
| `rx.checkbox("label")` | `checked`, `default_checked`, `name`, `disabled` | `bool` |
| `rx.switch` | `checked`, `default_checked`, `name` | `bool` |
| `rx.radio_group(items)` | `value`, `default_value`, `direction`, `name` | `str` |
| `rx.slider` | `default_value=[50]`, `min`, `max`, `step` | `list[float]` |
| `rx.upload` | see [Uploads](#17-file-upload-download-and-assets) | — |
| `rx.form` | `on_submit`, `reset_on_submit`, `id` | — |

### 11.3 Other controls in one example

```python
class PrefsState(rx.State):
    dark: bool = False
    volume: int = 50
    color: str = "blue"

    @rx.event
    def set_dark(self, value: bool):
        self.dark = value

    @rx.event
    def set_volume(self, value: list[float]):
        self.volume = int(value[0])

    @rx.event
    def set_color(self, value: str):
        self.color = value


rx.vstack(
    rx.switch(checked=PrefsState.dark, on_change=PrefsState.set_dark),
    rx.slider(default_value=[50], on_change=PrefsState.set_volume),
    rx.radio_group(["red", "blue", "green"], value=PrefsState.color, on_change=PrefsState.set_color),
    rx.text(PrefsState.dark.to_string(), " / ", PrefsState.volume, " / ", PrefsState.color),
)
```

**How it works:** each control gives its own kind of value (`bool`, `list[float]`, `str`), so the handler's type hint must match.

### 11.4 Validation pattern

```python
class RegisterState(rx.State):
    password: str = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value

    @rx.var
    def password_error(self) -> str:
        if not self.password:
            return ""
        if len(self.password) < 8:
            return "At least 8 characters"
        return ""


rx.vstack(
    rx.input(type="password", value=RegisterState.password, on_change=RegisterState.set_password),
    rx.cond(RegisterState.password_error != "", rx.text(RegisterState.password_error, color="red")),
)
```

**How it works:** computed vars are perfect for validation messages — they update live and can use normal Python (`len`, `if`) because they run on the server.

### 11.5 Clearing an input with `rx.set_value`

```python
rx.input(id="chat-input", placeholder="Message")
rx.button("Clear", on_click=rx.set_value("chat-input", ""))
```

[↑ Back to top](#table-of-contents)

---

## 12. Routing and Navigation

### 12.1 Static, dynamic and catch-all routes

| Route pattern | Example URL | Access value in a handler |
|---|---|---|
| `/about` | `/about` | — |
| `/user/[id]` | `/user/42` | `self.router.page.params["id"]` |
| `/blog/[year]/[slug]` | `/blog/2026/hello` | `params["year"]`, `params["slug"]` |
| `/docs/[...rest]` | `/docs/a/b/c` | `params["rest"]` (the matched segments) |
| `/docs/[[...rest]]` | `/docs` or `/docs/a/b` | optional catch-all |
| any + query string | `/search?q=reflex` | `params["q"]` |

```python
class UserState(rx.State):
    name: str = ""

    @rx.event
    def load_user(self):
        user_id = self.router.page.params.get("id", "")
        self.name = f"User #{user_id}"


@rx.page(route="/user/[id]", on_load=UserState.load_user)
def user_page() -> rx.Component:
    return rx.heading(UserState.name)
```

**How it works:** the square brackets in the route define a URL parameter. `on_load` runs each time someone lands on the page, reads the parameter from `self.router`, and fills the state. Path and query parameters both appear in `page.params`.

### Quick reference: `self.router` (read inside handlers)

| Attribute | Contains |
|---|---|
| `self.router.page.path` | Route pattern, e.g. `/user/[id]` |
| `self.router.page.raw_path` | Actual URL path, e.g. `/user/42` |
| `self.router.page.params` | Dict of dynamic + query parameters |
| `self.router.session.client_token` | Unique id of this browser tab |
| `self.router.session.session_id` | Socket session id |
| `self.router.session.client_ip` | Client IP |
| `self.router.headers.host` | Host header |
| `self.router.headers.user_agent` | Browser user-agent string |

### 12.2 Navigating

```python
rx.link("About", href="/about")                                   # internal link (no page reload)
rx.link("Docs", href="https://reflex.dev/docs", is_external=True) # external
rx.button("Go", on_click=rx.redirect("/dashboard"))                # from a button
rx.button("Open docs", on_click=rx.redirect("https://reflex.dev", is_external=True))
```

```python
@rx.event
def after_login(self):
    return rx.redirect("/dashboard")        # from a handler
```

### 12.3 Navbar with active-link highlight

```python
def nav_link(label: str, href: str) -> rx.Component:
    active = rx.State.router.page.path == href      # a Var: compares the current route
    return rx.link(
        label,
        href=href,
        weight=rx.cond(active, "bold", "regular"),
        color=rx.cond(active, rx.color("accent", 11), rx.color("gray", 11)),
    )


def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading("MyApp", size="5"),
        rx.spacer(),
        nav_link("Home", "/"),
        nav_link("About", "/about"),
        padding="1em",
        width="100%",
    )
```

**How it works:** `rx.State.router.page.path` is available as a Var in components, so you can style the link of the current page.

### 12.4 Avoiding the "blank flash" before the app is ready

```python
def index() -> rx.Component:
    return rx.cond(
        rx.State.is_hydrated,
        main_content(),
        rx.center(rx.spinner(), height="100vh"),
    )
```

**How it works:** `is_hydrated` turns `True` after the browser connects and loads initial state. Showing a spinner until then avoids clicks landing before events are wired (also very handy for E2E tests).

[↑ Back to top](#table-of-contents)

---

## 13. Tables, Charts and Data Display

### 13.1 Tables

```python
import dataclasses


@dataclasses.dataclass
class Employee:
    name: str
    role: str
    salary: int


class HrState(rx.State):
    staff: list[Employee] = [Employee("Ada", "Engineer", 120), Employee("Grace", "Admiral", 150)]


def row(e: Employee) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(e.name),
        rx.table.cell(e.role),
        rx.table.cell(e.salary),
    )


rx.table.root(
    rx.table.header(
        rx.table.row(
            rx.table.column_header_cell("Name"),
            rx.table.column_header_cell("Role"),
            rx.table.column_header_cell("Salary"),
        )
    ),
    rx.table.body(rx.foreach(HrState.staff, row)),
    variant="surface",
    width="100%",
)
```

**How it works:** `root → header → row → column_header_cell` for headings and `body → row → cell` for data. `rx.foreach` builds one `row` per item.

### Quick reference: table parts

| Component | HTML equivalent | Purpose |
|---|---|---|
| `rx.table.root` | `<table>` | Wrapper (`variant="surface"\|"ghost"`, `size`) |
| `rx.table.header` | `<thead>` | Header group |
| `rx.table.body` | `<tbody>` | Body group |
| `rx.table.row` | `<tr>` | Row |
| `rx.table.column_header_cell` | `<th>` | Column heading |
| `rx.table.row_header_cell` | `<th scope=row>` | Row heading |
| `rx.table.cell` | `<td>` | Data cell |

### 13.2 Quick data grid with `rx.data_table`

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ada", "Linus"], "age": [36, 55]})

rx.data_table(data=df, pagination=True, search=True, sort=True)

# or with plain lists:
rx.data_table(
    data=[["Ada", 36], ["Linus", 55]],
    columns=["Name", "Age"],
    pagination=True,
    search=True,
    sort=True,
)
```

**How it works:** gives you search, sort and pagination for free. For editable grids use `rx.data_editor`.

### 13.3 Charts with Recharts

```python
data = [
    {"month": "Jan", "sales": 400, "cost": 240},
    {"month": "Feb", "sales": 300, "cost": 139},
    {"month": "Mar", "sales": 520, "cost": 280},
]

rx.recharts.bar_chart(
    rx.recharts.bar(data_key="sales", fill=rx.color("accent", 8)),
    rx.recharts.bar(data_key="cost", fill=rx.color("gray", 8)),
    rx.recharts.x_axis(data_key="month"),
    rx.recharts.y_axis(),
    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
    rx.recharts.graphing_tooltip(),
    rx.recharts.legend(),
    data=data,          # a list of dicts — or a State var: ChartState.data
    width="100%",
    height=300,
)
```

**How it works:** a chart is a wrapper (`bar_chart`) that receives `data=` (list of dicts), plus child elements: the series (`bar`), axes (`x_axis`/`y_axis`), grid, tooltip, legend. `data_key` picks the dict key to plot. Pass a State var as `data` to make it live.

### Quick reference: chart types

| Chart wrapper | Series element | Common props |
|---|---|---|
| `rx.recharts.bar_chart` | `rx.recharts.bar` | `data_key`, `fill`, `stack_id` |
| `rx.recharts.line_chart` | `rx.recharts.line` | `data_key`, `stroke`, `type_="monotone"` |
| `rx.recharts.area_chart` | `rx.recharts.area` | `data_key`, `fill`, `stroke` |
| `rx.recharts.pie_chart` | `rx.recharts.pie` | `data`, `data_key`, `name_key`, `inner_radius` |
| `rx.recharts.scatter_chart` | `rx.recharts.scatter` | `data`, `fill` |
| `rx.recharts.radar_chart` | `rx.recharts.radar` | `data_key`, `fill` |
| `rx.recharts.composed_chart` | mix of bar/line/area | — |
| Shared helpers | `x_axis`, `y_axis`, `cartesian_grid`, `graphing_tooltip`, `legend`, `reference_line` | — |

### 13.4 Plotly

```python
import plotly.express as px
import plotly.graph_objects as go


class PlotState(rx.State):
    @rx.var
    def fig(self) -> go.Figure:
        return px.line(x=[1, 2, 3], y=[3, 1, 2])


rx.plotly(data=PlotState.fig)
```

**How it works:** build a Plotly figure in Python, return it from a computed var typed `go.Figure`, and render with `rx.plotly`.

### 13.5 Other data-display components

| Component | Use |
|---|---|
| `rx.data_editor` | Editable spreadsheet-like grid |
| `rx.moment` | Formatted/relative dates ("3 minutes ago") |
| `rx.list.ordered` / `rx.list.unordered` / `rx.list.item` | Lists |
| `rx.data_list.root` / `.item` | Label–value pairs |
| `rx.progress`, `rx.badge`, `rx.avatar` | Status widgets |

[↑ Back to top](#table-of-contents)

---

## 14. Database with `rx.Model`

> Needs the DB extras on 0.9.9+: `pip install "reflex[db]"`.

### 14.1 Configure the database

```python
# rxconfig.py
config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",       # default; use Postgres in production:
    # db_url="postgresql+psycopg://user:pass@host:5432/dbname",
)
```

### 14.2 Define models

```python
class Note(rx.Model, table=True):        # table=True => real DB table
    title: str
    body: str = ""
    done: bool = False
```

**How it works:** `rx.Model` is built on **SQLModel** (SQLAlchemy + pydantic). `table=True` creates the table, and an auto-incrementing integer `id` primary key is added for you. Field types map to columns.

### 14.3 CRUD in a State

```python
from sqlmodel import select


class NoteState(rx.State):
    notes: list[Note] = []

    @rx.event
    def load(self):
        with rx.session() as session:
            self.notes = session.exec(select(Note).order_by(Note.id.desc())).all()

    @rx.event
    def add(self, form_data: dict):
        with rx.session() as session:
            session.add(Note(title=form_data["title"]))
            session.commit()
        return NoteState.load                     # refresh the list

    @rx.event
    def toggle(self, note_id: int):
        with rx.session() as session:
            note = session.get(Note, note_id)
            if note:
                note.done = not note.done
                session.add(note)
                session.commit()
        return NoteState.load

    @rx.event
    def delete(self, note_id: int):
        with rx.session() as session:
            note = session.get(Note, note_id)
            if note:
                session.delete(note)
                session.commit()
        return NoteState.load
```

```python
def note_row(n: Note) -> rx.Component:
    return rx.hstack(
        rx.checkbox(checked=n.done, on_change=lambda _: NoteState.toggle(n.id)),
        rx.text(n.title),
        rx.icon_button(rx.icon("trash-2"), variant="ghost", on_click=NoteState.delete(n.id)),
    )


@rx.page(route="/notes", on_load=NoteState.load)
def notes() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.hstack(rx.input(name="title", placeholder="New note"), rx.button("Add", type="submit")),
            on_submit=NoteState.add,
            reset_on_submit=True,
        ),
        rx.foreach(NoteState.notes, note_row),
    )
```

**How it works:**

- `with rx.session() as session:` opens a DB session and closes it automatically.
- `select(Note)` builds a query; `session.exec(...).all()` runs it and returns model objects, which you can store directly in a `list[Note]` var.
- Every write ends with `session.commit()`.
- Handlers return `NoteState.load` to re-query after changes.

### Quick reference: session and query methods

| Call | Purpose |
|---|---|
| `rx.session()` | Sync DB session (use with `with`) |
| `rx.asession()` | Async DB session (needs `async_db_url`, use with `async with`) |
| `session.add(obj)` / `session.add_all([...])` | Stage inserts/updates |
| `session.commit()` | Save changes |
| `session.refresh(obj)` | Reload object from DB |
| `session.rollback()` | Undo uncommitted changes |
| `session.get(Model, id)` | Fetch by primary key |
| `session.delete(obj)` | Delete a row |
| `session.exec(select(Model))` | Run a query → `.all()`, `.first()`, `.one()` |
| `select(M).where(M.done == False)` | Filter |
| `select(M).order_by(M.id.desc())` | Sort |
| `select(M).limit(20).offset(40)` | Paginate |

### 14.4 Migrations

```bash
reflex db init                                   # once: creates alembic config
reflex db makemigrations --message "add note"    # after changing models
reflex db migrate                                # apply
```

**How it works:** Reflex uses **Alembic**. Whenever you add/rename columns after data exists, generate and apply a migration so the database matches your models.

[↑ Back to top](#table-of-contents)

---

## 15. Browser Storage and Cookies

```python
class PrefState(rx.State):
    theme: str = rx.Cookie("light")                              # cookie named "theme"
    token: str = rx.LocalStorage("", name="auth_token")          # localStorage key "auth_token"
    draft: str = rx.SessionStorage("")                           # cleared when the tab closes

    @rx.event
    def set_theme(self, value: str):
        self.theme = value

    @rx.event
    def logout(self):
        return [rx.remove_cookie("theme"), rx.remove_local_storage("auth_token")]
```

**How it works:** these special var types are **stored in the browser** and loaded into state on the next visit. Read and write them like normal vars.

### Quick reference: storage var types

| Type | Persists | Constructor arguments |
|---|---|---|
| `rx.Cookie` | Until `max_age`/session end; sent with HTTP requests | `rx.Cookie(default, name=None, path="/", max_age=None, domain=None, secure=None, same_site="lax")` |
| `rx.LocalStorage` | Until cleared; per browser | `rx.LocalStorage(default, name=None, sync=False)` — `sync=True` syncs across tabs |
| `rx.SessionStorage` | Until the tab closes | `rx.SessionStorage(default, name=None)` |

> **Security:** anything in browser storage is **user-controlled**. Never treat a cookie or local-storage value as proof of identity by itself — store an opaque random token and verify it on the server (see next section).

[↑ Back to top](#table-of-contents)

---

## 16. Authentication Patterns

Reflex has no built-in login system — you assemble one from state, cookies and a database, or use a community package (e.g. `reflex-local-auth`, or provider integrations such as Clerk or Google sign-in). Below is a minimal do-it-yourself pattern so you understand the moving parts.

### 16.1 Models

```python
import secrets
import bcrypt                                   # pip install bcrypt
from sqlmodel import select


class User(rx.Model, table=True):
    username: str
    password_hash: str


class AuthSession(rx.Model, table=True):
    user_id: int
    token: str
```

### 16.2 Auth state

```python
class AuthState(rx.State):
    auth_token: str = rx.Cookie("", name="auth_token", max_age=60 * 60 * 24 * 7)
    error: str = ""

    def _current_user_id(self) -> int | None:            # underscore => NOT an event handler
        if not self.auth_token:
            return None
        with rx.session() as session:
            row = session.exec(select(AuthSession).where(AuthSession.token == self.auth_token)).first()
            return row.user_id if row else None

    @rx.event
    def register(self, form_data: dict):
        hashed = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt()).decode()
        with rx.session() as session:
            session.add(User(username=form_data["username"], password_hash=hashed))
            session.commit()
        return rx.redirect("/login")

    @rx.event
    def login(self, form_data: dict):
        with rx.session() as session:
            user = session.exec(select(User).where(User.username == form_data["username"])).first()
            if user and bcrypt.checkpw(form_data["password"].encode(), user.password_hash.encode()):
                token = secrets.token_urlsafe(32)
                session.add(AuthSession(user_id=user.id, token=token))
                session.commit()
                self.auth_token = token
                self.error = ""
                return rx.redirect("/dashboard")
        self.error = "Invalid username or password"

    @rx.event
    def logout(self):
        with rx.session() as session:
            for s in session.exec(select(AuthSession).where(AuthSession.token == self.auth_token)).all():
                session.delete(s)
            session.commit()
        self.auth_token = ""
        return rx.redirect("/login")

    @rx.event
    def require_login(self):
        if self._current_user_id() is None:
            return rx.redirect("/login")
```

### 16.3 Guarding a page

```python
@rx.page(route="/dashboard", on_load=AuthState.require_login)
def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Secret dashboard"),
        rx.button("Log out", on_click=AuthState.logout),
    )
```

**How it works:**

1. Passwords are **hashed with bcrypt**, never stored in plain text.
2. On login the server creates a random **session token**, saves it in the DB and gives it to the browser as a cookie.
3. On protected pages `require_login` looks the token up on the server. No valid session → redirect.
4. Also check permissions **inside every sensitive handler**, not only on page load — a user can trigger handlers without visiting the page.
5. In production serve over **HTTPS** and set `secure=True` on the cookie.

[↑ Back to top](#table-of-contents)

---

## 17. File Upload, Download and Assets

### 17.1 Upload

```python
from pathlib import Path


class UploadState(rx.State):
    uploaded: list[str] = []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            safe_name = Path(file.filename).name            # strip any folder parts
            (rx.get_upload_dir() / safe_name).write_bytes(data)
            self.uploaded.append(safe_name)


def upload_ui() -> rx.Component:
    return rx.vstack(
        rx.upload(
            rx.text("Drag and drop files here or click to select"),
            id="upload1",
            multiple=True,
            accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
            max_files=3,
            border="1px dashed gray",
            padding="2em",
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),   # names picked so far
        rx.button("Upload", on_click=UploadState.handle_upload(rx.upload_files(upload_id="upload1"))),
        rx.button("Clear", on_click=rx.clear_selected_files("upload1")),
        rx.foreach(UploadState.uploaded, lambda n: rx.image(src=rx.get_upload_url(n), width="120px")),
    )
```

**How it works:** the `rx.upload` zone only *selects* files. Clicking **Upload** triggers `handle_upload` with `rx.upload_files(upload_id=...)`, which sends the selected files to the backend. The handler is `async`, reads bytes, and saves them into Reflex's upload folder. `rx.get_upload_url(name)` gives a URL to display them.

### Quick reference: `rx.upload` and helpers

| Item | Purpose |
|---|---|
| `rx.upload(children, id=..., ...)` | The drop zone |
| `multiple` | Allow several files |
| `accept={"mime/type": [".ext", ...]}` | Restrict file types |
| `max_files`, `max_size` (bytes) | Limits |
| `no_click`, `no_drag`, `disabled` | Turn interactions off |
| `on_drop` | Run a handler as soon as files are dropped |
| `rx.selected_files(id)` | Var: names of currently selected files |
| `rx.clear_selected_files(id)` | Event: reset selection |
| `rx.upload_files(upload_id=...)` | Event arg: send files to a handler |
| `rx.cancel_upload(id)` | Cancel an in-progress upload |
| `rx.get_upload_dir()` | `Path` to the upload folder on the server |
| `rx.get_upload_url(filename)` | URL to serve an uploaded file |

> Always sanitize filenames, restrict `accept`, and set `max_size` — uploads are untrusted input.

### 17.2 Download

```python
@rx.event
def export_csv(self):
    return rx.download(data="name,age\nAda,36\n", filename="people.csv")

@rx.event
def get_manual(self):
    return rx.download(url="/manual.pdf")           # a file placed in assets/
```

### 17.3 Static assets

- Files in the project's `assets/` folder are served from the site root: `assets/logo.png` → `rx.image(src="/logo.png")`.
- For files kept next to your Python code use `rx.asset("logo.png")` (returns a content-hashed URL, so browsers never serve stale copies; use `shared=True` for a file shared across modules).
- Add a favicon by placing `favicon.ico` in `assets/`.
- Add scripts with `rx.script(src="...")`; add CSS files with `stylesheets=[...]` on `rx.App`.


[↑ Back to top](#table-of-contents)

---

## 18. Backend API and Lifespan Tasks

### 18.1 Adding your own HTTP endpoints

The Reflex backend is an ASGI app. To add REST endpoints (webhooks, mobile clients, health checks), pass a FastAPI (or Starlette) app as `api_transformer`:

```python
from fastapi import FastAPI

api = FastAPI(title="My API")


@api.get("/api/health")
async def health():
    return {"status": "ok"}


@api.post("/api/webhook")
async def webhook(payload: dict):
    # verify signatures here!
    return {"received": True}


app = rx.App(api_transformer=api)
```

**How it works:** Reflex mounts its own routes (websocket, upload) into your FastAPI app, so your endpoints live on the same backend port (`http://localhost:8000/api/health`). Older tutorials use `app.api.add_api_route(...)` — prefer `api_transformer` in current versions.

### 18.2 Background jobs for the whole server (lifespan tasks)

```python
import asyncio


async def cleanup_expired_sessions():
    while True:
        await asyncio.sleep(3600)          # every hour
        ...                                # e.g. delete old rows


app = rx.App()
app.register_lifespan_task(cleanup_expired_sessions)
```

**How it works:** the coroutine starts when the server starts and is cancelled on shutdown. Use it for periodic jobs that don't belong to any one user session (use `@rx.event(background=True)` for per-user work).

### 18.3 Calling external APIs from handlers

```python
import httpx


class WeatherState(rx.State):
    city: str = "Paris"
    temp: str = ""

    @rx.event
    def set_city(self, value: str):
        self.city = value

    @rx.event
    async def fetch(self):
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://wttr.in/" + self.city, params={"format": "%t"})
        self.temp = resp.text
```

**How it works:** use **async** HTTP clients (`httpx.AsyncClient`) inside `async def` handlers so waiting on the network doesn't block other users.

### 18.4 Exception handling and other settings

- Backend errors are shown in the terminal running `reflex run`; frontend/state mismatches are reported back to the backend log too.
- Configure cross-origin access with `cors_allowed_origins` in `rx.Config`.
- Built-in admin UI for your models: `rx.App(admin_dash=rx.AdminDash(models=[Note]))`.

[↑ Back to top](#table-of-contents)

---

## 19. Custom Components

### 19.1 Function components (simplest)

```python
def labeled_input(label: str, **props) -> rx.Component:
    return rx.vstack(rx.text(label, size="2", weight="bold"), rx.input(**props), spacing="1")


labeled_input("Email", name="email", type="email")
```

**How it works:** forward extra keyword arguments with `**props` so callers can still set any prop of the inner component.

### 19.2 `rx.memo` (performance-optimized reusable components)

```python
@rx.memo
def user_badge(name: rx.Var[str], online: rx.Var[bool]) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=name[:2], size="2"),
        rx.text(name),
        rx.cond(online, rx.badge("online", color_scheme="green")),
    )


rx.foreach(UserState.users, lambda u: user_badge(name=u.name, online=u.online))
```

**How it works:** `@rx.memo` compiles the component once and wraps it in React's `memo`, so it only re-renders when its props actually change. **Annotate every parameter as `rx.Var[...]`** and the return type as `rx.Component` (bare Python types still work but are deprecated). Great for list items and heavy widgets.

### 19.3 Stateful reusable components with `rx.ComponentState`

```python
class LikeButton(rx.ComponentState):
    likes: int = 0                                    # each instance has its OWN state

    @rx.event
    def like(self):
        self.likes += 1

    @classmethod
    def get_component(cls, **props):
        return rx.button(rx.icon("heart"), cls.likes, on_click=cls.like, **props)


like_button = LikeButton.create

rx.hstack(like_button(), like_button())               # two independent counters
```

**How it works:** a normal `rx.State` is one shared blueprint per session; `rx.ComponentState` creates **separate state per component instance**. `get_component` builds the UI from `cls.<var>` and `cls.<handler>`.

### 19.4 Wrapping a React library

```python
class ColorPicker(rx.Component):
    library = "react-colorful"                       # npm package
    tag = "HexColorPicker"                           # exported component name
    color: rx.Var[str]                               # prop
    on_change: rx.EventHandler[lambda color: [color]]  # event: what args to send to Python


color_picker = ColorPicker.create


class PickerState(rx.State):
    color: str = "#db114b"

    @rx.event
    def set_color(self, value: str):
        self.color = value


rx.vstack(
    color_picker(color=PickerState.color, on_change=PickerState.set_color),
    rx.text(PickerState.color),
)
```

**How it works:** you describe an existing npm component: which `library`, which `tag` (component name), what **props** it takes (typed with `rx.Var[...]`), and how its **events** map to Python arguments. Reflex adds the dependency and generates the import.

### Quick reference: wrapping attributes

| Attribute / helper | Purpose |
|---|---|
| `library = "pkg@version"` | npm package (pin a version) |
| `tag = "Name"` | Exported component name |
| `alias = "Other"` | Rename on import to avoid clashes |
| `is_default = True` | Package uses a *default* export |
| `lib_dependencies = ["dep"]` | Extra npm packages needed |
| `rx.NoSSRComponent` (base class) | For browser-only libs that break during server rendering |
| `add_imports()` | Extra imports (dict) |
| `add_custom_code()` | Extra JS at module level |
| `add_hooks()` | React hooks to run inside the component |
| `rx.EventHandler[lambda ...]` | Declares an event and its argument mapping |
| `rx.Var[T]` | Typed prop |

> If you wrote a custom component against `react-router-dom`, change the library to `react-router` on Reflex 0.9.9+.

### 19.5 JavaScript interop

```python
class ScrollState(rx.State):
    ua: str = ""

    @rx.event
    def to_top(self):
        return rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})")

    @rx.event
    def ask_ua(self):
        return rx.call_script("navigator.userAgent", callback=ScrollState.got_ua)

    @rx.event
    def got_ua(self, ua: str):
        self.ua = ua
```

Load third-party scripts with `rx.script(src="https://example.com/lib.js")` inside a page or `head_components`.

[↑ Back to top](#table-of-contents)

---

## 20. Configuration and Plugins

```python
# rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="my_app",
    frontend_port=3000,
    backend_port=8000,
    db_url="sqlite:///reflex.db",
    telemetry_enabled=False,
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV4Plugin()],
    default_color_mode="system",
)
```

### Quick reference: common `rx.Config` options

| Option | Purpose |
|---|---|
| `app_name` | **Required.** Must match your package folder |
| `frontend_port`, `backend_port` | Ports (defaults `3000`, `8000`) |
| `backend_host` | Interface to bind (`0.0.0.0` inside containers) |
| `api_url` | Public URL of the backend (needed when frontend and backend are hosted separately) |
| `deploy_url` | Public URL of the frontend |
| `frontend_path` | Serve the app from a sub-path (e.g. `/app`) |
| `db_url` / `async_db_url` | Database connection strings (sync / async) |
| `redis_url` | Redis for multi-worker / multi-instance state |
| `redis_token_expiration` | How long idle client state is kept in Redis |
| `cors_allowed_origins` | Origins allowed to talk to the backend |
| `telemetry_enabled` | Anonymous usage stats on/off |
| `loglevel` | `debug`, `info`, `warning`, `error`, `critical` |
| `plugins` / `disable_plugins` | Enable/disable build plugins |
| `default_color_mode` | `"system"`, `"light"`, `"dark"` |
| `frozen_lockfile` | Fail fast when the frontend lockfile is out of date (default on) |
| `frontend_packages` | Extra npm packages to install |
| `env_file` | Path to a `.env` file to load |
| `show_built_with_reflex` | Toggle the "Built with Reflex" badge |

**Environment variables:** every option can also be set from the environment (recent versions use a `REFLEX_` prefix, e.g. `REFLEX_DEFAULT_COLOR_MODE`); use them for secrets and per-environment values instead of hard-coding.

### Quick reference: built-in plugins

| Plugin | Purpose |
|---|---|
| `rx.plugins.SitemapPlugin()` | Generates `sitemap.xml` |
| `rx.plugins.TailwindV4Plugin()` | Tailwind CSS v4 |
| `rx.plugins.TailwindV3Plugin()` | Tailwind CSS v3 |

[↑ Back to top](#table-of-contents)

---

## 21. Testing with Playwright

Because a Reflex app is just a website, **end-to-end tests with Playwright** fit naturally. Keep pure logic in helper functions (unit-testable) and use Playwright for user flows.

### 21.1 Make elements easy to find

```python
rx.heading(State.count, custom_attrs={"data-testid": "count"})
rx.button("+", id="inc", on_click=State.increment)
```

**How it works:** `id=` sets the HTML id; `custom_attrs={...}` adds any attribute (great for `data-testid`). Roles and visible text (`get_by_role`, `get_by_text`) work too.

### 21.2 A pytest fixture that starts the app

(Linux/macOS version; on Windows replace the `killpg` calls with `taskkill /T /F /PID <pid>`.)

```python
# tests/conftest.py
import os
import signal
import subprocess
import time
import urllib.request

import pytest

BASE_URL = "http://localhost:3000"


@pytest.fixture(scope="session", autouse=True)
def reflex_server():
    proc = subprocess.Popen(["reflex", "run"], start_new_session=True)   # new process group
    for _ in range(180):                                                  # wait up to ~3 min
        try:
            urllib.request.urlopen(BASE_URL, timeout=2)
            break
        except Exception:
            time.sleep(1)
    else:
        os.killpg(proc.pid, signal.SIGTERM)
        raise RuntimeError("Reflex did not start")
    yield
    os.killpg(proc.pid, signal.SIGTERM)                                   # stop node + python children
```

### 21.3 The tests

```bash
pip install pytest pytest-playwright
playwright install chromium
```

```python
# tests/test_counter.py
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def test_counter_increments(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_test_id("count")).to_have_text("0")    # waits until the app hydrated

    page.get_by_role("button", name="+").click()
    expect(page.get_by_test_id("count")).to_have_text("1")


def test_form_shows_toast(page: Page):
    page.goto(f"{BASE_URL}/signup")
    page.get_by_placeholder("Your name").fill("Ada")
    page.get_by_role("button", name="Sign up").click()
    expect(page.get_by_text("Welcome, Ada!")).to_be_visible()
```

**How it works:** Playwright's `expect(...)` **retries until the condition is true** (default 5 s), which suits async state updates over the websocket. Clicks happen immediately though, so on slow machines render the page behind `rx.cond(rx.State.is_hydrated, ...)` (see [Routing](#124-avoiding-the-blank-flash-before-the-app-is-ready)) so the button doesn't exist until events are wired.

### 21.4 Tips

| Tip | Why |
|---|---|
| Use a **separate SQLite file** for tests (`db_url` via env var) | Tests never touch real data |
| Prefer `get_by_role`, `get_by_test_id` | Stable against copy/style changes |
| Run with `--headed --slowmo 300` while debugging | See what the browser does |
| Use `page.pause()` or `playwright codegen http://localhost:3000` | Record selectors interactively |
| In CI start the server in a step, wait for the port, then run pytest | Same as the fixture above |
| For in-process harnesses Reflex ships `reflex.testing.AppHarness` (install `reflex[testing]`) | It is what Reflex's own integration tests use — check its current signature in the source before relying on it |

[↑ Back to top](#table-of-contents)

---

## 22. Deployment and Scaling

### 22.1 Production build

```bash
reflex run --env prod            # optimized frontend + backend on your machine
reflex export                    # produces frontend.zip and backend.zip to host yourself
reflex export --frontend-only    # static frontend only (host on any static host/CDN)
```

### 22.2 Options at a glance

| Option | How | Good for |
|---|---|---|
| **Reflex Cloud** | `reflex login` then `reflex deploy` | Fastest path, managed hosting |
| **Docker on a VPS/Kubernetes** | Container running `reflex run --env prod` behind a reverse proxy | Full control |
| **Split hosting** | Static frontend on a CDN + backend container | Global static delivery; set `api_url` to the backend URL |
| **Sub-path hosting** | `frontend_path="/myapp"` | App lives at `example.com/myapp` |

### 22.3 A starting-point Dockerfile

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl unzip && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN reflex init
EXPOSE 8000
CMD ["reflex", "run", "--env", "prod", "--single-port", "--backend-host", "0.0.0.0"]
```

**How it works:** installs dependencies, initializes the project, and serves frontend + backend on one port (`--single-port`). Put it behind HTTPS (Caddy, Nginx, a cloud load balancer). Treat this as a template and cross-check the official self-hosting docs for your version (Node requirements change).

### 22.4 Scaling checklist

- **State lives in server memory per session.** With more than one backend worker/instance, set `redis_url` so all instances share state.
- Use a **real database** (Postgres) instead of SQLite in production.
- Put secrets in **environment variables**, not source code.
- Set `api_url` and `cors_allowed_origins` correctly when frontend and backend are on different domains.
- Enable HTTPS and set `secure=True` on auth cookies.
- Structured logs: `REFLEX_LOG_JSON=1` (or `reflex run --json`).
- Observability: the optional `reflex-otel` package adds OpenTelemetry tracing.

[↑ Back to top](#table-of-contents)

---

## 23. Performance and Best Practices

| Do | Why |
|---|---|
| Keep State small; put big datasets in the DB or a `_backend_var` | Every changed var is serialized to the browser |
| Use **computed vars** for filtering/sorting/formatting | They cache and only recompute when inputs change |
| **Debounce** typing events (`.debounce(300)`) for search boxes | Fewer round-trips |
| **Paginate** long lists (`limit/offset`) | Rendering thousands of rows is slow |
| Use `@rx.memo` for list items and heavy widgets | Avoids re-rendering unchanged parts |
| Use `async def` + `httpx.AsyncClient` for I/O | Doesn't block other users |
| Use `background=True` for long jobs | UI stays responsive |
| `yield` to show progress | Users see something happen |
| Split State by feature (`AuthState`, `CartState`, `SearchState`) | Smaller, clearer, faster |
| Add type hints everywhere | Reflex uses them; editors catch bugs |
| Validate on the server even if the UI validates | Handlers can be called by anyone |
| Keep secrets in `_backend_vars` or env vars | They never reach the browser |
| Commit `reflex.lock/` and `requirements.txt` | Reproducible builds |
| Use `rx.color(...)` instead of hex colors | Automatic dark-mode support |

[↑ Back to top](#table-of-contents)

---

## 24. Common Errors and Gotchas

### Quick reference: error → fix

| Symptom (approximate message) | Cause | Fix |
|---|---|---|
| "Cannot convert Var to bool" / using `if State.x:` | Python control flow on a Var | Use `rx.cond(...)` or `rx.match(...)` |
| `len()` / `str()` / `sum()` on a Var fails | Builtins don't work on Vars | `State.items.length()`, `State.n.to_string()`, or compute in a `@rx.var` |
| `foreach` complains about type / missing annotation | Untyped list var | Annotate: `items: list[str] = []` |
| "Computed var must have a return type annotation" | Missing `-> type` on `@rx.var` | Add the return annotation |
| Error when reading `self.x` in a background task | Access outside the lock | Wrap in `async with self:` |
| State doesn't update after mutating a nested object | Reflex can't see the mutation | Re-assign the var: `self.items = [...]` |
| "Failed to serialize" / not JSON serializable | Non-serializable value in a var | Convert to str/dict, or store it in a `_backend_var` |
| Handler argument type mismatch error | `on_change` passes `str`, handler expects `int` (or other mismatch) | Fix the hint or convert inside the handler |
| Button "does nothing" | You wrote `on_click=State.f()` or `on_click=f` (a plain function) | Use `on_click=State.f` (or `State.f(arg)`) |
| `SetUndefinedStateVarError` / `set_x` not found | Relying on removed auto-setters | Write `def set_x(self, value)` yourself |
| Page never appears / 404 | `@rx.page` module never imported | Import it in the main module |
| Second `rx.App()` raises `ReflexRuntimeError` | 0.9.9+ allows one app per process | Reuse one app (or fork the registration context in tests) |
| Node version error at start | Node older than required | Install Node ≥ 22.22 |
| Blank page / stale UI after upgrading | Old build artifacts | Stop the server, delete `.web/`, run `reflex run` again |
| UI stops reacting; terminal shows a "client error" | Frontend and backend out of sync | Reload the page after the frontend rebuild; check `api_url` |
| Port already in use | Another process | `reflex run --frontend-port 3001 --backend-port 8001` |
| `ImportError: pydantic` / `rx.Model` errors after `pip install reflex` | pydantic became optional in 0.9.9 | `pip install "reflex[db]"` or `"reflex[pydantic]"` |
| Works locally, fails in prod | `api_url` / CORS / HTTPS misconfigured | Set `api_url` to the public backend URL and allow origins |

### Gotcha list

1. **`self.x` vs `State.x`** — `self.` only in handlers; `State.` in components.
2. **Handlers are not called with `()` in the UI** — pass `State.handler` or `State.handler(arg)`.
3. **Public methods on State become handlers** — prefix helpers with `_`.
4. **Both `rx.cond` branches are built** — don't put expensive work in them.
5. **Only one copy of state per browser tab** — never use module-level globals for per-user data.
6. **Globals are shared between users** — use them only for read-only config and caches.
7. **Backend vars (`_x`) cannot be used in components.**
8. **Don't mutate `rx.Model` objects and expect the DB to change** — call `session.add()` + `session.commit()`.
9. **`time.sleep` blocks** — use `await asyncio.sleep`.

[↑ Back to top](#table-of-contents)

---

## 25. Full Example Projects

### 25.1 Todo app (state only, computed vars, filters)

```python
# todo/todo.py
import dataclasses
import reflex as rx


@dataclasses.dataclass
class Todo:
    id: int
    text: str
    done: bool = False


class TodoState(rx.State):
    todos: list[Todo] = []
    new_text: str = ""
    filter: str = "all"
    _next_id: int = 1                                   # backend counter

    @rx.var
    def visible(self) -> list[Todo]:
        if self.filter == "active":
            return [t for t in self.todos if not t.done]
        if self.filter == "done":
            return [t for t in self.todos if t.done]
        return self.todos

    @rx.var
    def remaining(self) -> int:
        return sum(1 for t in self.todos if not t.done)

    @rx.event
    def set_new_text(self, value: str):
        self.new_text = value

    @rx.event
    def set_filter(self, value: str):
        self.filter = value

    @rx.event
    def handle_key(self, key: str):
        if key == "Enter":
            return TodoState.add

    @rx.event
    def add(self):
        text = self.new_text.strip()
        if not text:
            return
        self.todos.append(Todo(self._next_id, text))
        self._next_id += 1
        self.new_text = ""

    @rx.event
    def toggle(self, todo_id: int):
        self.todos = [
            Todo(t.id, t.text, not t.done) if t.id == todo_id else t for t in self.todos
        ]

    @rx.event
    def remove(self, todo_id: int):
        self.todos = [t for t in self.todos if t.id != todo_id]


def todo_row(t: Todo) -> rx.Component:
    return rx.hstack(
        rx.checkbox(checked=t.done, on_change=lambda _: TodoState.toggle(t.id)),
        rx.text(t.text, flex="1", text_decoration=rx.cond(t.done, "line-through", "none")),
        rx.icon_button(rx.icon("trash-2"), variant="ghost", color_scheme="red",
                       on_click=TodoState.remove(t.id)),
        width="100%",
        align="center",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Todos", size="8"),
            rx.hstack(
                rx.input(
                    value=TodoState.new_text,
                    on_change=TodoState.set_new_text,
                    on_key_down=TodoState.handle_key,
                    placeholder="What needs doing?",
                    flex="1",
                ),
                rx.button("Add", on_click=TodoState.add),
                width="100%",
            ),
            rx.segmented_control.root(
                rx.segmented_control.item("All", value="all"),
                rx.segmented_control.item("Active", value="active"),
                rx.segmented_control.item("Done", value="done"),
                value=TodoState.filter,
                on_change=TodoState.set_filter,
            ),
            rx.foreach(TodoState.visible, todo_row),
            rx.text(TodoState.remaining, " items left", color_scheme="gray"),
            spacing="4",
            width="100%",
            padding_y="2em",
        ),
        size="2",
    )


app = rx.App(theme=rx.theme(accent_color="violet"))
app.add_page(index, title="Todos")
```

**How it works**

- `Todo` is a dataclass so rows have typed fields (`t.text`, `t.done`).
- `visible` and `remaining` are **computed vars** — the filter buttons and counter update automatically.
- `on_key_down=TodoState.handle_key` receives the key name; on `"Enter"` it returns the `add` handler (chaining).
- `toggle` rebuilds the list (simple and always detected); `remove` filters it.
- `_next_id` is a backend var — the UI doesn't need it.

### 25.2 Streaming chat with a local or hosted LLM

This uses any **OpenAI-compatible** streaming endpoint (for example a local Ollama server at `http://localhost:11434/v1`, or a hosted API — set the URL, model and key accordingly).

```python
# chat/chat.py
import json
import httpx
import reflex as rx

API_URL = "http://localhost:11434/v1/chat/completions"
MODEL = "llama3.2"


class ChatState(rx.State):
    messages: list[dict[str, str]] = []
    prompt: str = ""
    streaming: bool = False

    @rx.event
    def set_prompt(self, value: str):
        self.prompt = value

    @rx.event(background=True)
    async def send(self):
        async with self:
            text = self.prompt.strip()
            if self.streaming or not text:
                return
            self.messages.append({"role": "user", "content": text})
            history = [dict(m) for m in self.messages]           # plain dict copies
            self.messages.append({"role": "assistant", "content": ""})
            self.prompt = ""
            self.streaming = True

        payload = {"model": MODEL, "messages": history, "stream": True}
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", API_URL, json=payload) as resp:
                    async for line in resp.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        chunk = line[6:]
                        if chunk == "[DONE]":
                            break
                        delta = json.loads(chunk)["choices"][0]["delta"].get("content") or ""
                        if delta:
                            async with self:
                                self.messages[-1]["content"] += delta   # live token stream
        except Exception as exc:
            async with self:
                self.messages[-1]["content"] = f"Error: {exc}"
        finally:
            async with self:
                self.streaming = False


def bubble(m: dict[str, str]) -> rx.Component:
    is_user = m["role"] == "user"
    return rx.box(
        rx.markdown(m["content"]),
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
        bg=rx.cond(is_user, rx.color("accent", 4), rx.color("gray", 3)),
        padding="0.75em 1em",
        border_radius="12px",
        max_width="80%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Chat", size="7"),
            rx.vstack(rx.foreach(ChatState.messages, bubble), width="100%", spacing="3"),
            rx.hstack(
                rx.input(
                    id="prompt",
                    value=ChatState.prompt,
                    on_change=ChatState.set_prompt,
                    placeholder="Ask something…",
                    flex="1",
                ),
                rx.button("Send", on_click=ChatState.send, loading=ChatState.streaming),
                width="100%",
            ),
            spacing="4",
            width="100%",
            padding_y="2em",
        ),
        size="2",
    )


app = rx.App()
app.add_page(index, title="Chat")
```

**How it works**

1. `send` is a **background** handler so the UI stays free while tokens arrive.
2. The first `async with self:` block appends the user message and an empty assistant message, then releases the lock.
3. We call the model with an async streaming HTTP request; for each `data:` line we parse the delta.
4. Each token is appended inside a short `async with self:` block — leaving the block pushes the update to the browser, so text appears live.
5. `finally` always resets `streaming`, even on errors, so the button never stays stuck.
6. `rx.markdown` renders the model's Markdown (code blocks, lists).

[↑ Back to top](#table-of-contents)

---

## 26. Cheat Sheet and Resources

### 26.1 "I want to…" cheat sheet

| I want to… | Write |
|---|---|
| Show a var | `rx.text(State.x)` |
| Change a var on click | `rx.button("Go", on_click=State.go)` |
| Pass an argument | `on_click=State.go(5)` |
| Bind an input | `rx.input(value=State.q, on_change=State.set_q)` |
| Submit a form | `rx.form(..., on_submit=State.submit)` |
| Show/hide | `rx.cond(State.flag, a, b)` |
| Switch on a value | `rx.match(State.s, ("a", A), ("b", B), default)` |
| Loop | `rx.foreach(State.items, render)` |
| Derived value | `@rx.var def total(self) -> int: ...` |
| Run on page open | `@rx.page(on_load=State.load)` |
| Navigate | `rx.redirect("/x")` / `rx.link(href="/x")` |
| Notify | `return rx.toast.success("Done")` |
| Long/async work | `@rx.event(background=True)` + `async with self:` |
| Live progress | `yield` inside a handler |
| Read a URL parameter | `self.router.page.params["id"]` |
| Save to DB | `with rx.session() as s: s.add(obj); s.commit()` |
| Persist in browser | `rx.Cookie` / `rx.LocalStorage` var |
| Upload a file | `rx.upload(...)` + `rx.upload_files(...)` |
| Dark/light toggle | `rx.color_mode.button()` |
| Add an API route | `rx.App(api_transformer=fastapi_app)` |
| Reusable component | plain function, or `@rx.memo` |
| Wrap a React package | subclass `rx.Component` with `library` + `tag` |
| Test in a browser | Playwright against `localhost:3000` |
| Deploy | `reflex deploy` or `reflex export` + Docker |

### 26.2 Handy links

| Resource | URL |
|---|---|
| Official docs | https://reflex.dev/docs/ |
| Component library reference | https://reflex.dev/docs/library/ |
| API reference: App | https://reflex.dev/docs/api-reference/app/ |
| API reference: State | https://reflex.dev/docs/api-reference/state/ |
| API reference: Var | https://reflex.dev/docs/api-reference/var/ |
| API reference: Config | https://reflex.dev/docs/api-reference/config/ |
| API reference: CLI | https://reflex.dev/docs/api-reference/cli/ |
| API reference: Special events | https://reflex.dev/docs/api-reference/special-events/ |
| API reference: Browser storage | https://reflex.dev/docs/api-reference/browser-storage/ |
| Changelog (check before upgrading) | https://reflex.dev/docs/changelog/ |
| Docs index for AI tools | https://reflex.dev/docs/llms.txt |
| Source code | https://github.com/reflex-dev/reflex |
| Community | https://discord.gg/T5WSbC2YtQ |

> **Tip:** on any docs page, remove the trailing slash and append `.md` to read its Markdown version — handy to paste into an AI assistant when you're stuck.

### 26.3 Suggested learning path

1. Build the **counter** ([Section 4](#4-your-first-app)), then the **Todo app** ([25.1](#251-todo-app-state-only-computed-vars-filters)).
2. Practice **State + events** until `self.x` vs `State.x` feels natural ([8](#8-state-and-vars), [9](#9-events-and-event-handlers)).
3. Add **routing + navbar + template** ([5](#5-the-app-object-and-pages), [12](#12-routing-and-navigation)).
4. Add a **database** and **auth** ([14](#14-database-with-rxmodel), [16](#16-authentication-patterns)).
5. Style with **themes/responsive props** ([7](#7-styling-and-theming)).
6. Write **Playwright tests** ([21](#21-testing-with-playwright)) and **deploy** ([22](#22-deployment-and-scaling)).

*End of guide — happy building!*

[↑ Back to top](#table-of-contents)
