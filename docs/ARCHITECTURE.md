# Lumora Copy Trading Platform

## Architecture Decisions

---

### AD-001

Title:
Package Controls Lot Size

Decision:

The server never sends lot size.

The client receives the user's package and uses the configured lot size.

Reason:

- Business flexibility
- Easy package upgrades
- Prevent user manipulation

Status:

APPROVED

---

### AD-002

Title:

Magic Number Protection

Decision:

Every trade executed by Lumora must contain a generated MT5 Magic Number.

Reason:

- Protect manual trades
- Protect other EAs
- Safe close operations

Status:

APPROVED

---

### AD-003

Title:

Signal UUID

Decision:

Every signal must have a UUID.

Reason:

- Global uniqueness
- Future analytics
- Client execution reports

Status:

APPROVED

---

### AD-004

Title:

Package / Plan Separation

Decision:

Packages and Plans are different entities.

Package:

- Gold
- Platinum

Plan:

- Trial
- Monthly
- Lifetime

Reason:

Allows flexible pricing.

Status:

APPROVED

---

### AD-005

Title:

Architecture Freeze

Decision:

No new features will be added to V1.

Future features must be added to the roadmap.

Status:

APPROVED

AD-006

Title:
Subscription History

Decision:
Subscriptions are immutable.

Old subscriptions are never overwritten.

A new subscription record is created for every activation or renewal.

Reason:
Complete customer history.
Better reporting.
Future analytics.

Status:
APPROVED

### AD-007

Title:
Soft State Management

Decision:

Business records are never deleted.

Statuses are updated instead.

Examples:

Subscription:
Active
Expired
Cancelled

Payment:
Pending
Approved
Rejected

Reason:

Complete audit history.

Status:

APPROVED