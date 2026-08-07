# Lumora Coding Rules

---

## Money

Always use:

Numeric(10,2)

Never use:

Float

---

## Passwords

bcrypt only

Never store plain text.

---

## Authentication

JWT only

Use security.py wrappers.

---

## Database

Use Foreign Keys.

Never duplicate data.

---

## Constants

Use shared enums.

Never hardcode strings.

---

## Logging

Never use print() in production modules.

Always use the shared logger.

---

## Architecture

One module per step.

Every module must:

Design

↓

Code

↓

Run

↓

Test

↓

Lock

↓

Next