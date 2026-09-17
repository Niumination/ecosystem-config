# Pi Authentication Flow — Sequence Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Pi       │     │  App     │     │  App Studio  │     │  Pi Platform │
│  Browser  │     │  Frontend│     │  Backend     │     │  API         │
└────┬─────┘     └────┬─────┘     └──────┬───────┘     └──────┬───────┘
     │                │                  │                    │
     │  1. Load page  │                  │                    │
     │───────────────>│                  │                    │
     │                │                  │                    │
     │  2. Pi.init()  │                  │                    │
     │<───────────────│                  │                    │
     │                │                  │                    │
     │  3. Pi.authenticate()              │                    │
     │<───────────────│                  │                    │
     │                │                  │                    │
     │  4. accessToken                    │                    │
     │───────────────>│                  │                    │
     │                │                  │                    │
     │                │  5. POST /pi/auth/v1/login            │
     │                │─────────────────>│                    │
     │                │                  │                    │
     │                │                  │  6. Verify token   │
     │                │                  │───────────────────>│
     │                │                  │                    │
     │                │                  │  7. User info      │
     │                │                  │<───────────────────│
     │                │                  │                    │
     │                │  8. sessionToken │                    │
     │                │<─────────────────│                    │
     │                │                  │                    │
     │  9. Display    │                  │                    │
     │<───────────────│                  │                    │
     │                │                  │                    │
```

## Key Points

- Step 1-2: Load Pi SDK and initialize
- Step 3-4: User authenticates via Pi Browser popup
- Step 5-8: Exchange accessToken for sessionToken via App Studio
- Step 9: Display verified username from App Studio

## CRITICAL

- NEVER use `uid` or `username` from `Pi.authenticate()` for authorization
- ONLY trust values returned by App Studio backend (`session.user`)
- The `accessToken` is short-lived — exchange it immediately
